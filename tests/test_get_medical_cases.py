from app.models.models import MedicalCase
from app import db

def test_get_medical_cases(client, app):
    clear_medical_cases_table(app)
    response = client.get("/dermoapp/medical-cases/v1/medical-cases")
    data = response.json
    code = response.status
    assert data['message'] == 'Listado de casos medicos'
    assert code == '200 OK'

def clear_medical_cases_table(app):
    with app.app_context():
        medical_cases = MedicalCase.query.all()
        for medical_case in medical_cases:
            db.session.delete(medical_case)
            db.session.commit()
            db.session.close()