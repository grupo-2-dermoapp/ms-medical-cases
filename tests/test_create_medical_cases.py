from app.utils.utils import uuid4Str

def test_create_medical_case_with_bad_data(client):
    response = client.post("/dermoapp/medical-cases/v1/medical-cases", json={})
    data = response.json
    code = response.status
    assert data['message'] == 'Error en la petición'
    assert code == '400 BAD REQUEST'

def test_create_medical_case_with_valid_data(client):
    patient = create_patient(client)

    payload = {}
    payload['type_of_injury'] = 'TAINT'
    payload['shape_of_injury'] = 'RING'
    payload['number_of_injuries'] = 'LONELY'
    payload['injury_distribucion'] = 'ASYMMETRIC'
    payload['body_part'] = 'FOREHEAD'
    payload['type_of_diagnosis'] = 'DOCTOR'
    payload['patient_uuid'] = patient['uuid']
    response = client.post("/dermoapp/medical-cases/v1/medical-cases", json=payload)
    data = response.json
    code = response.status
    assert data['message'] == 'Error en la petición'
    assert code == '400 BAD REQUEST'

def create_patient(client):
    payload = {}
    payload['uuid'] = uuid4Str()
    payload['location'] = 'test'
    response = client.post("/dermoapp/medical-cases/v1/patients", json=payload)
    if (response.status == '201 CREATED'):
        return payload
    else:
        return {}
    