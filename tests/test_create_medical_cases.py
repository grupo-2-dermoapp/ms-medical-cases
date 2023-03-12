def create_medical_case_with_bad_data(client):
    response = client.post("/dermoapp/medical-cases/v1/medical-cases", json={})
    data = response.json
    code = response.status
    assert data['message'] == 'Error en la petición'
    assert code == '400 BAD REQUEST'