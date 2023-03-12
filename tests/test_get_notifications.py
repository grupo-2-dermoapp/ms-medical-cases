def get_notifications(client):
    uuid_test = 'test'
    response = client.get("/dermoapp/medical-cases/v1/notification-history/{}".format(uuid_test))
    data = response.json
    code = response.status
    assert data['message'] == 'Listado de notificaciones'
    assert code == '200 OK'