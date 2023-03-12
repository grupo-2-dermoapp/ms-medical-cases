def get_medical_cases_with_bad_id(client):
    uuid_test = 'test'
    response = client.get("/dermoapp/medical-cases/v1/medical-cases/{}".format(uuid_test))
    data = response.json
    code = response.status
    assert data['message'] == 'No se pudo completar la solicitud'
    assert code == '400 BAD REQUEST'