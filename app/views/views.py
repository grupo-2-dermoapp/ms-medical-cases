# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request
import requests
from app.models.models import Patient, Doctor, MedicalCase, MedicalDiagnostic, db
from app.models.models import MedicalCaseSchema, MedicalDiagnosticSchema
from app.models.models import Notification, NotificationSchema
import os
from sqlalchemy.exc import IntegrityError
from app.utils.utils import send_notification
from faker import Faker
import random

fake = Faker()

class Health(Resource):
    def get(self):
        data = {
            "message" : "OK"
        }
        return data, 200

class DoctorView(Resource):
    def post(self):
        request_data = request.json
        try:
            doctor =  Doctor(
                uuid = request_data['uuid'],
                location = request_data['location']
            )
            db.session.add(doctor)
            db.session.commit()
            data = {
                "message" : "OK"
            }
            return data, 201
        except IntegrityError as e:
            data = {
                "message" : "fail"
            }
            return data, 400 
        finally:
            db.session.close()

class PatientView(Resource):
    def post(self):
        request_data = request.json
        try:
            patient =  Patient(
                uuid = request_data['uuid'],
                location = request_data['location']
            )
            db.session.add(patient)
            db.session.commit()
            data = {
                "message" : "OK"
            }
            return data, 201
        except IntegrityError:
            data = {
                "message" : "fail"
            }
            return data, 400 
        finally:
            db.session.close()

class MedicalCaseView(Resource):
    def post(self):
        request_data = request.json
        try:
            medical_case = MedicalCase(
                type_of_injury = request_data['type_of_injury'],
                shape_of_injury = request_data['shape_of_injury'],
                number_of_injuries = request_data['number_of_injuries'],
                injury_distribucion = request_data['injury_distribucion'],
                body_part = request_data['body_part'],
                type_of_diagnosis = request_data['type_of_diagnosis'],
                patient_uuid = request_data['patient_uuid']
            )


            db.session.add(medical_case)
            db.session.commit()

            medical_case_data = {
                "uuid" : str(medical_case.uuid),
                "location": "/dermoapp/medical-cases/v1/medical-cases/" + str(medical_case.uuid),
                "patient_uuid" : request_data['patient_uuid']
            }

            requests.post(
            os.getenv('CLINICAL_HISTORY_SERVICE')+"/dermoapp/clinical-history/v1/medical-cases",
            json=medical_case_data)

            if medical_case.type_of_diagnosis.name == 'AUTO':
                medical_diagnostic = MedicalDiagnostic(
                    name_of_injury = fake.text(max_nb_chars=24),
                    diagnosis = fake.text(max_nb_chars=200),
                    treatment = fake.text(max_nb_chars=200),
                    certification_percentage = str(random.randrange(70,100)),
                    medical_case_uuid = medical_case.uuid
                )

                db.session.add(medical_diagnostic)
                db.session.commit()

                data = {
                    "code": "1201",
                    "message" : "Caso médico registrado correctamente",
                    "medical_diagnostic" : {
                        "uuid" : medical_diagnostic.uuid,
                        "diagnosis" : medical_diagnostic.diagnosis,
                        "treatment" : medical_diagnostic.treatment,
                        "certification_percentage" : medical_diagnostic.certification_percentage
                    }
                }

                return data, 201

            data = {
                "code": "1200",
                "message" : "Caso médico registrado correctamente",
            }

            return data, 201
        
        except Exception as e:
            db.session.rollback()

            data = {
                "code": "1202",
                "message" : "Error en la petición"
            }

            return data, 400
        
        finally:
            db.session.close_all()

    def get(self):
        medical_cases_list = []
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 2, type=int)
        medical_cases = db.session.query(MedicalCase).filter(
            MedicalCase.doctor_uuid == None,
            MedicalCase.type_of_diagnosis != 'AUTO'
        ).paginate(page=page, per_page=per_page)

        for medical_case in medical_cases.items:
            patient = db.session.query(Patient).filter(
                Patient.uuid == medical_case.patient_uuid).first()
            patient_request_response = requests.get(
                os.getenv('AUTH_SERVICE')+str(patient.location))

            if patient_request_response.status_code == 200:
                patient_info = patient_request_response.json()
                patient_data = {
                    "names" : patient_info["names"]
                }
                medical_case_data = MedicalCaseSchema().dump(medical_case)
                medical_case_data['patient'] = patient_data
            else:
                patient_data = {
                    "names" : "Sin Nombre"
                }
                medical_case_data = MedicalCaseSchema().dump(medical_case)
                medical_case_data['patient'] = patient_data

            medical_cases_list.append(medical_case_data)
        
        pagination_data = {
            "page" : medical_cases.page,
            "pages" : medical_cases.pages,
            "total_data" : medical_cases.total,
            "prev_num" : medical_cases.prev_num,
            "next_num" : medical_cases.next_num,
            "has_next" : medical_cases.has_next,
            "has_prev" : medical_cases.has_prev
        }

        data = {
            "code" : "1210",
            "message" : "Listado de casos medicos",
            "medical_cases" : medical_cases_list,
            "paginator" : pagination_data
        }

        return data, 200
    
class MedicalCaseById(Resource):
    def get(self, medical_case_uuid):
        medical_case = MedicalCase.query.filter_by(
            uuid=medical_case_uuid
        ).first()

        if medical_case:
            data = {
                "code" : "",
                "message" : "Información del caso médico",
                "medical_case" : MedicalCaseSchema().dump(medical_case)
            }

            return data, 200
        
        else:
            data = {
                "code" : "",
                "message" : "No se pudo completar la solicitud"
            }

            return data, 400
    
class MedicalDiagnosticView(Resource):
    def post(self):
        request_data = request.json
        try:
            medical_diagnostic = MedicalDiagnostic(
                name_of_injury = request_data['name_of_injury'],
                diagnosis = request_data['diagnosis'],
                treatment = request_data['treatment'],
                medical_case_uuid = request_data['medical_case_uuid'],
                doctor_uuid = request_data['doctor_uuid']
            )

            db.session.add(medical_diagnostic)
            

            data = {
                "code": "1250",
                "message" : "Diagnostico medico registrado"
            }

            medical_case = MedicalCase.query.filter_by(
                uuid = request_data['medical_case_uuid']
            ).first()

            patient = db.session.query(Patient).filter(
                Patient.uuid == medical_case.patient_uuid).first()

            patient_request_response = requests.get(
                os.getenv('AUTH_SERVICE')+str(patient.location))
            
            if patient_request_response.status_code == 200:
                patient_info = patient_request_response.json()
                notification_token = patient_info["notification_token"]
                title = 'Diagnostico recibido'
                message = 'Un doctor ha realizado el diagnostico de tu caso medico'
                send_notification(
                    title=title,
                    message=message,
                    token=notification_token)
                
                notification = Notification(
                    title=title,
                    message=message,
                    patient_uuid=medical_case.patient_uuid
                )

                db.session.add(notification)

            db.session.commit()   
            return data, 201
        
        except:
            db.session.rollback()

            data = {
                "code": "1251",
                "message" : "Error en la petición"
            }

            return data, 400
        
        finally:
            db.session.close()

class MedicalDiagnosticByMedicalCaseview(Resource):
    def get(self, medical_case_uuid):
        medical_case = MedicalCase.query.filter_by(
            uuid = medical_case_uuid
        ).first()

        if not medical_case:
            data = {
                "code" : "",
                "message" : "No se pudo completar la solicitud"
            }
            return data, 400

        medical_diagnostic = MedicalDiagnostic.query.filter_by(
            medical_case_uuid = medical_case.uuid
        ).first()

        if not medical_diagnostic:
            data = {
                "code" : "",
                "message" : "No se pudo completar la solicitud"
            }
            return data, 400
        
        data = {
            "code" : "",
            "message" : "",
            "medical_diagnostic" : MedicalDiagnosticSchema().dump(medical_diagnostic),
        }

        return data, 200
    
class HistoryPatientNotificationView(Resource):
    def get(self, patient_uuid):
        notifications_list = []
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 2, type=int)
        notifications = db.session.query(Notification).filter(
            Notification.patient_uuid == patient_uuid
        ).paginate(page=page, per_page=per_page)

        for notification in notifications.items:
            notifications_list.append(
                NotificationSchema().dump(notification))

        pagination_data = {
            "page" : notifications.page,
            "pages" : notifications.pages,
            "total_data" : notifications.total,
            "prev_num" : notifications.prev_num,
            "next_num" : notifications.next_num,
            "has_next" : notifications.has_next,
            "has_prev" : notifications.has_prev
        }

        data = {
            "code" : "",
            "message" : "Listado de notificaciones",
            "notifications" : notifications_list,
            "paginator" : pagination_data
        }

        return data, 200

class ReportView(Resource):
    def get(self, doctor_uuid):

        pass
