# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request, current_app
import validators
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.models.models import Patient, Doctor, MedicalCase, MedicalDiagnostic, db
from app.models.models import MedicalCaseSchema, MedicalDiagnosticSchema
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import get_jwt_identity, get_jwt
import random
import json
import app


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
            doctor =  Patient(
                uuid = request_data['uuid'],
                location = request_data['location']
            )
            db.session.add(doctor)
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

            if medical_case.type_of_diagnosis.name == 'AUTO':
                medical_diagnostic = MedicalDiagnostic(
                    name_of_injury = "Diagnostico automatico",
                    diagnosis = "Diagnostico automatico",
                    treatment = "Diagnostico automatico",
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
                os.getenv('AUTH_SERVICE')+patient.location)

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
            db.session.commit()

            data = {
                "code": "1250",
                "message" : "Diagnostico medico registrado"
            }

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