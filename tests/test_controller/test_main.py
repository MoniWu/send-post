#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest

from app.models import User, db


@pytest.mark.usefixtures("test_http_client")
class TestMain:
    def test_home(self, test_http_client):
        """ Tests if the home page loads """

        rv = test_http_client.get('api/1.0/')
        assert rv.status_code == 200

    def test_user_info(self, test_http_client):
        user1 = User('00000000010', "123456")
        user2 = User('00000000011', "123456")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        token1 = test_http_client.post('/api/1.0/login', json={
            'phonenum': '00000000010',
            'password': "123456"
        }).get_json()['token']

        token2 = test_http_client.post('/api/1.0/login', json={
            'phonenum': '00000000011',
            'password': "123456"
        }).get_json()['token']

        user1 = User.query.filter_by(phonenum="00000000010").first()
        user2 = User.query.filter_by(phonenum="00000000011").first()

        assert token1 == user1.token
        assert token2 == user2.token

        user_info1 = test_http_client.get('/api/1.0/user_info',
                                          headers={'Authorization': "Bear " + token1}).get_json()['data']
        user_info2 = test_http_client.get('/api/1.0/user_info',
                                          headers={'Authorization': "Bear " + token2}).get_json()['data']

        assert user_info1['user_phone'] == user1.phonenum
        assert user_info2['user_phone'] == user2.phonenum
        assert user_info2['last_login_at'] == str(user2.last_login_at)
