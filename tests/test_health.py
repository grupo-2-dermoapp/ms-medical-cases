def test_service_is_alive(client):
    response = client.get("/dermoapp/auth/v1/health")
    data = response.json
    assert "OK" == data['message']

    
