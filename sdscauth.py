from flask import Flask, redirect, request, render_template
from jose import jwt
from openid_connect import OpenIDClient
import os

API_URL = os.environ.get('API_URL', 'http://localhost:9000/')
API_URL_RM = os.environ.get('API_URL_RM', 'http://localhost:9000/')
KEYCLOAK_URL = os.environ.get('KEYCLOAK_URL', 'https://testing.datascience.ch:8080/auth/realms/SDSC/')
CLIENT_ID = os.environ.get('CLIENT_ID', 'ddosa-client')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET','90e2b9a4-ddda-4588-ab64-33dab06389a1')

class KeycloakClient(OpenIDClient):
    def get_id(self, token_response):
        return jwt.decode(
            token_response.id_token,
            self.keys,
            algorithms=['RS256'],
            options={'verify_at_hash': False},
            audience=self.client_id,
            issuer=self.issuer,
            access_token=token_response.access_token, )


@app.route("/")
def redirecting():
    c = KeycloakClient(KEYCLOAK_URL, CLIENT_ID, CLIENT_SECRET)

    code = request.args.get('code', '')

    if not code:
        return redirect(c.authorize(request.base_url, None))

    v = c.request_token(request.base_url, code)

    return render_template(
        'api.html', api_url=API_URL, token=v.access_token, user=v.userinfo,
        auth_url=KEYCLOAK_URL, own_url=request.base_url, api_url_rm=API_URL_RM)
