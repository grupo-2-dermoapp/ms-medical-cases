from app.views.views import Health, DoctorView, PatientView
from app.views.views import MedicalCaseView, MedicalDiagnosticView
from app.views.views import MedicalCaseById, MedicalDiagnosticByMedicalCaseview
from app.views.views import HistoryPatientNotificationView, ReportView

from flask_restful import Api
from flask_cors import CORS
from app import create_app
from flask_migrate import upgrade
from app import db

import pytest

@pytest.fixture()
def app():

    # settings_module = os.getenv('APP_SETTINGS_MODULE')
    settings_module = 'config.develop.Test'
    app = create_app(settings_module)
    db.init_app(app)

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
    # Completarlo con lo del entrypoint
    
    # with app.app_context():
    #         upgrade()

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()