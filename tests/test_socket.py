# NOTE https://github.com/miguelgrinberg/Flask-socket_app/blob/main/test_socket_app.py
def test_socket_should_conneted(app, socket_app):
    client = socket_app.test_client(app, auth={"foo": "bar"})
    client2 = socket_app.test_client(app, auth={"foo": "bar"})
    assert client.is_connected()
    assert client2.is_connected()
    assert client.eio_sid != client2.eio_sid

    received = client.get_received()
    assert len(received) == 3
    assert received[0]["args"] == "connected"

    client.disconnect()
    assert not client.is_connected()
    assert client2.is_connected()
    client2.disconnect()
    assert not client2.is_connected()


def test_send_message_should_received(app, socket_app):
    client = socket_app.test_client(app, auth={'foo': 'bar'})
    client.get_received()
    client.send('echo this message back')
    received = client.get_received()
    assert len(received) == 1
    assert received[0]['args'] == 'echo this message back'

def test_send_json_should_share_data(app, socket_app):
    client1 = socket_app.test_client(app, auth={'foo': 'bar'})
    client2 = socket_app.test_client(app, auth={'foo': 'bar'})
    client1.get_received()
    client2.get_received()
    client1.send({'a': 'b'}, json=True)
    received = client1.get_received()

    assert len(received)==1
    assert received[0]['args']['a'] == 'b'
    received = client2.get_received()
    assert len(received) == 1
    assert received[0]['args']['a'] == 'b'

def test_custom_event_should_work(app, socket_app):
    client = socket_app.test_client(app, auth={'foo': 'bar'})
    client.get_received()
    client.emit('my custom event', {'a': 'b'})
    received = client.get_received()
    assert len(received) == 1
    assert len(received[0]['args']) == 1
    assert received[0]['name'] == 'my custom response'
    assert received[0]['args'][0]['a'] == 'b'

def test_broadcast_namespace(app, socket_app):
    client1 = socket_app.test_client(app, namespace='/test')
    client2 = socket_app.test_client(app, namespace='/test')
    client3 = socket_app.test_client(app, auth={'foo': 'bar'})
    received = client2.get_received('/test')
    assert len(received) == 3

    client3.get_received()
    client1.emit('my custom broadcast namespace event', {'a': 'b'},
                    namespace='/test')
    received = client2.get_received('/test')

    assert len(received) == 1
    assert len(received[0]['args']) == 1
    assert received[0]['name'] == 'my custom namespace response'
    assert received[0]['args'][0]['a'] == 'b'
    assert len(client3.get_received()) == 0
