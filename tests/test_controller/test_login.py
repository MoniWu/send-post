import pytest

from app.models import User, db

create_user = True


@pytest.mark.usefixtures("test_http_client")
class TestLogin:
    def test_login(self, test_http_client):
        """ Tests if the login form functions """
        user = User('00000000000', "123456")
        db.session.add(user)
        db.session.commit()

        data = {
            'phonenum': '00000000000',
            'password': "123456"
        }
        rv = test_http_client.post('/api/1.0/login', json=data)
        data = rv.get_json()
        assert rv.status_code == 200
        assert 'Logged in successfully.' in str(data['message'])

    def test_login_fail(self, test_http_client):
        """ Tests if the login form fails correctly """

        user = User('00000000001', "123456")
        db.session.add(user)
        db.session.commit()

        data = {
            'phonenum': '00000000001',
            'password': "12345"
        }
        rv = test_http_client.post('/api/1.0/login', json=data)
        data = rv.get_json()
        assert rv.status_code == 200
        assert 'Logged in successfully.' not in str(data['message'])
