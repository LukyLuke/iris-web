#!/usr/bin/env python3
#
#  IRIS Source Code
#  Copyright (C) 2021 - Airbus CyberSecurity (SAS)
#  ir@cyberactionlab.net
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import re
from unittest import TestCase

from flask import url_for
from flask.testing import FlaskClient

from app import app


class TestHelper(TestCase):
    @staticmethod
    def log_in(test_app: FlaskClient) -> None:
        login_page = test_app.get('/login')

        csrf_token = re.search(r'id="csrf_token" name="csrf_token" type="hidden" value="(.*?)"', str(login_page.data)).group(1)

        test_app.post('/login', data=dict(username='tester', password='<test_password>', csrf_token=csrf_token), follow_redirects=True)

    def verify_path_without_cid_redirects_correctly(self, path: str, assert_string: str):
        with app.test_client() as test_app:
            self.log_in(test_app)

            result = test_app.get(url_for(path))

            self.assertEqual(302, result.status_code)
            self.assertIn(assert_string, str(result.data))

            result2 = test_app.get(url_for(path), follow_redirects=True)

            self.assertEqual(200, result2.status_code)

    def verify_path_with_cid(self, path: str, cid: str):
        with app.test_client() as test_app:
            self.log_in(test_app)

            payload = {'cid': cid}
            result = test_app.get(url_for(path, **payload))

            self.assertEqual(200, result.status_code)

    def verify_path(self, path: str):
        with app.test_client() as test_app:
            self.log_in(test_app)

            result = test_app.get(url_for(path))

            self.assertEqual(200, result.status_code)

    def verify_response_with_cid(self, path: str, cid: str, excpected_response):
        with app.test_client() as test_app:
            self.log_in(test_app)

            payload = {'cid': cid}
            result = test_app.get(url_for(path, **payload))

            self.assertEqual(200, result.status_code)

            self.assertEqual(excpected_response, result.data)
