def get_medical_cases(client):
    response = client.get("/dermoapp/medical-cases/v1/medical-cases")
    data = response.json
    code = response.status
    assert data['message'] == 'Listado de casos medicos'
    assert code == '200 OK'