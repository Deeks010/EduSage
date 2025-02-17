import webbrowser
from flask import Flask, request, redirect, session
import requests
from dotenv import load_dotenv
import os
import threading

load_dotenv()

class LinkedInAuthApp:
    def __init__(self):
        self.CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
        self.REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI')
        self.CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.app1 = Flask(__name__)
        self.app1.secret_key = os.urandom(24)  # Generate a more secure secret key

        # Define routes
        self.app1.add_url_rule('/', 'home', self.home)
        self.app1.add_url_rule('/linkedin/login', 'linkedin_login', self.linkedin_login)
        self.app1.add_url_rule('/linkedin/callback', 'linkedin_callback', self.linkedin_callback)

    def home(self):
        session.clear()  # Clear the session when home route is accessed
        return 'Welcome to the LinkedIn OAuth demo! <a href="/linkedin/login">Login with LinkedIn</a>'

    def linkedin_callback(self):
        code = request.args.get('code')
        
        if code:
            user = str(input('Enter the name: '))  # This should be dynamic or based on the logged-in user's session
            access_token = self.get_access_token(code)
            if access_token:
                session['access_token'] = access_token
                uid = self.get_id(access_token)
                with open("details.txt", "a") as f:
                    f.write(f"access_token({user})={access_token}\n")
                    f.write(f"id({user})={uid}\n")
                return 'LinkedIn OAuth successful!'
            else:
                return 'Failed to get access token!'
        else:
            return 'LinkedIn OAuth failed!'


    def get_access_token(self, code):
        access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.REDIRECT_URI,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
        }
        response = requests.post(access_token_url, data=data)
        print(f"Response from LinkedIn access token request: {response.json()}")
        return response.json().get('access_token')

if __name__ == '__main__':
    app1 = LinkedInAuthApp()
    app1.run()
