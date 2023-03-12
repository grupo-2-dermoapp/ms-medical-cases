def create_medical_diagnostic_with_bad_data(client):
    response = client.post("/dermoapp/medical-cases/v1/medical-diagnostic", json={})
    data = response.json
    code = response.status
    assert data['message'] == 'Error en la petición'
    assert code == '400 BAD REQUEST'