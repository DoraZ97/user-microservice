from flask import Flask, Response
import database_services.RDBService as d_service
from flask_cors import CORS
from flask import jsonify, request
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import json
import os

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource

app = Flask(__name__)
CORS(app)

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
#
# app.secret_key = "supersekrit"
# blueprint = make_google_blueprint(
#     client_id="314377796932-bcks1e2lbvpi2v6crbb65alcgkpl6l9i.apps.googleusercontent.com",
#     client_secret="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",
#     scope=["profile", "email"]
# )
# app.register_blueprint(blueprint, url_prefix="/login")
#
# @app.route("/")
# def index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v1/userinfo")
#     assert resp.ok, resp.text
#     return "You are {email} on Google".format(email=resp.json()["email"])


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route('/imdb/artists/<prefix>')
def get_artists_by_prefix(prefix):
    res = IMDBArtistResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route('/users', methods=["GET", "POST", "UPDATE"])
def get_users():
    if request.method == 'GET':
        res = d_service.get_user("UserResource", "User")
        if not res:
            rsp = Response(json.dumps(res, default=str), status=404, content_type="application/json")
        else:
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    if request.method == 'POST':
        data = request.form
        tasks = {
            'ID': data.get('ID'),
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'email': data.get('email'),
            'addressID': data.get('addressID')
        }
        if tasks["ID"] is None or tasks["firstName"] is None or tasks["lastName"] is None or tasks["email"] is None or tasks["addressID"] is None:
            rsp = Response(json.dumps(None), status=400, content_type="application/json")
        else:
            res = d_service.update_users("UserResource", "User", tasks)
            rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
        return rsp
    if request.method == 'UPDATE':
        data = request.form


@app.route('/users/<ID>', methods=["GET"])
def get_users_by_ID(ID):
    res = d_service.get_userID("UserResource", "User", ID)
    if not res:
        rsp = Response(json.dumps(res, default=str), status=404, content_type="application/json")
    else:
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/users/<ID>/address', methods=["GET"])
def get_users_address_by_ID(ID):
    res = d_service.get_address_by_userID("UserResource", "User", "Address", ID)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/address', methods=["GET"])
def get_address():
    res = d_service.get_address("UserResource", "Address")
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp




# @app.route('/getUsers')
# def get_by_prefix():
#     res = d_service.get_user("UserResource", 'nameChart')
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
