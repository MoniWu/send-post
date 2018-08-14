#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest

from app.models import db, User

create_user = False


@pytest.mark.usefixtures("test_http_client")
class TestModels:
    def test_user_save(self, test_http_client):
        """ Test Saving the user model to the database """

        user = User('00000000000', '1')
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(phonenum="00000000000").first()
        assert user is not None

    def test_user_password(self, test_http_client):
        """ Test password hashing and checking """

        user = User('123456789', 'supersafepassword')

        assert user.phonenum == '123456789'
        assert user.check_password('supersafepassword')
