from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from app import create_app
from flask import jsonify
from flask_migrate import Migrate
from app.views.views import Health, DoctorView, PatientView
from app.views.views import MedicalCaseView, MedicalDiagnosticView
from app.views.views import MedicalCaseById, MedicalDiagnosticByMedicalCaseview
from app.views.views import HistoryPatientNotificationView, ReportView
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

api = Api(app)
CORS(app)

api.add_resource(Health, "/dermoapp/medical-cases/v1/health")
api.add_resource(DoctorView, "/dermoapp/medical-cases/v1/doctors")
api.add_resource(PatientView, "/dermoapp/medical-cases/v1/patients")
api.add_resource(MedicalCaseView, "/dermoapp/medical-cases/v1/medical-cases")
api.add_resource(MedicalCaseById, "/dermoapp/medical-cases/v1/medical-cases/<string:medical_case_uuid>")
api.add_resource(MedicalDiagnosticView, "/dermoapp/medical-cases/v1/medical-diagnostic")
api.add_resource(MedicalDiagnosticByMedicalCaseview, "/dermoapp/medical-cases/v1/medical-diagnostic/<string:medical_case_uuid>")
api.add_resource(HistoryPatientNotificationView, "/dermoapp/medical-cases/v1/notification-history/<string:patient_uuid>")
api.add_resource(ReportView, "/dermoapp/medical-cases/v1/report/<string:doctor_uuid>")


if __name__ == '__main__':
    app.run()