# #!/usr/bin/env python
# #
# # Copyright 2007 Google Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# #

import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

signup_form = """
<h2>Signup</h2>
<form action='/' method='post'>
    <table>
    <tbody>
    <tr>
    <td>
        <label for='username'>Username</label>
    </td>
    <td>
        <input type='text' name='username' value='%(username)s' required/>
    <td class='error'>%(user_error)s</td>
    </td>
    </tr>
    <tr>
    <td>
        <label for='password'>Password</label>
    </td>
    <td>
        <input type='password' name='password' required/>
    <td class='error'>%(pass_error)s</td>
    </td>
    </tr>
    <tr>
    <td>
        <label for='verify'>Verify Password</label>
    </td>
    <td>
        <input type='password' name='verify' required/>
    <td class='error'>%(verify_error)s</td>
    </td>
    </tr>
    <tr>
    <td>
        <label for='email'>Email (optional)</label>
    </td>
    <td>
        <input type='text' name='email' value='%(email)s'/>
    <td class='error'>%(email_error)s</td>
    </td>
    </tr>
    </tbody>
    </table>
  <input type='submit' value='submit'/>
</form>
"""


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def valid_pass(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)


def valid_email(email):
    if email == '':
        return True
    else:
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def write_form(self, username='', user_error='', pass_error='', verify_error='', email='', email_error=''):
        content = page_header + signup_form + page_footer
        self.response.write(content % {'username': username, 'user_error': user_error, 'pass_error': pass_error, 'verify_error': verify_error, 'email': email, 'email_error': email_error})


    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        username_check = valid_username(username)
        pass_check =  valid_pass(password)
        email_check = valid_email(email)

        user_error = ''
        pass_error = ''
        verify_error = ''
        email_error = ''

        if not(username_check and pass_check and email_check and (verify == password)):
            if not username_check:
                user_error = 'Please enter a valid username'

            if not pass_check:
                pass_error = 'Please enter a valid password'

            if verify != password:
                verify_error = 'Passwords do not match'

            if not(email_check or email == ''):
                email_error = 'Please enter a valid email address'

            self.write_form(username, user_error, pass_error, verify_error, email, email_error)

        else:
            user = self.request.get('username')
            greeting = '<h2>Welcome, ' + user + '!</h2>'
            self.response.write(greeting)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
