def test_service_is_alive(client):
    response = client.get("/dermoapp/medical-cases/v1/health")
    print(response)
    data = response.json
    assert "OK" == data['message']

    
