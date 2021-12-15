from flask import Flask, Response, session, render_template
import database_services.RDBService as d_service
from flask_cors import CORS
from flask import jsonify, request
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from middleware import security
import grequests

import json
import os

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# from application_services.imdb_artists_resource import IMDBArtistResource
# from application_services.UsersResource.user_service import UserResource

app = Flask(__name__, template_folder='template')
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

# @app.route("/")
# def index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v1/userinfo")
#     assert resp.ok, resp.text
#     return "You are {email} on Google".format(email=resp.json()["email"])
#


######################## Middleware ###########################################

# @app.before_request
# def before_request_func():
#     print("running before_request_func")
#     if not security.check_security(request, session):
#         return render_template('auth.html')
#
# @app.after_request
# def after_request_func(response):
#     print("running after_request_func")
#     return response

############################################################################

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route('/api/users', methods=["GET", "POST"])
def get_users():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        res = None

        if user_id:
            res = d_service.get_userID("UserResource", "User", user_id)
        else:
            res = d_service.get_user("UserResource", "User")

        if not res:
            rsp = Response(json.dumps(res, default=str), status=404, content_type="application/json")
        else:
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    if request.method == 'POST':
        data = request.form
        tasks = {
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'addressID': data.get('addressID')
        }
        if tasks["firstName"] is None or tasks["lastName"] is None or tasks["email"] is None or tasks["addressID"] is None:
            rsp = Response(json.dumps(None), status=400, content_type="application/json")
        else:
            res = d_service.update_users("UserResource", "User", tasks)
            rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
        return rsp

@app.route('/api/users/email', methods=["POST"])
def update_email():
    data = request.form
    ID = data.get('ID')
    email = data.get('email')
    if ID is None:
        rsp = Response(json.dumps(None), status=422, content_type="application/json")
    else:
        res = d_service.update_email("UserResource", "User", ID, email)
        rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    return rsp

#
# @app.route('/api/users/<ID>', methods=["GET"])
# def get_users_by_ID(ID):
#     res = d_service.get_userID("UserResource", "User", ID)
#     if not res:
#         rsp = Response(json.dumps(res, default=str), status=404, content_type="application/json")
#     else:
#         rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp

@app.route('/api/users/address', methods=["GET"])
def get_users_address_by_ID():
    user_id = request.args.get('user_id')
    if not user_id:
        raise Exception("[User.get_users_address_by_ID] Error parsing user_id from query selector.")
    res = d_service.get_address_by_userID("UserResource", "User", "Address", user_id)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/api/address', methods=["GET", "POST"])
def get_address():
    if request.method == "GET":
        res = d_service.get_address("UserResource", "Address")
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

    if request.method == 'POST':
        data = request.form
        tasks = {
            'streetNo': data.get('streetNo'),
            'streetName': data.get('streetName'),
            'city': data.get('city'),
            'region': data.get('region'),
            'countryCode': data.get('countryCode'),
            'postalCode': data.get('postalCode')
        }

        if tasks["streetNo"] is None or tasks["streetName"] is None or tasks[
            "city"] is None or tasks["region"] is None or tasks["countryCode"] is None or tasks["postalCode"] is None:
            rsp = Response(json.dumps(None), status=400, content_type="application/json")
        else:
            res = d_service.update_address("UserResource", "Address", tasks)
            rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
        return rsp

@app.route('/register', methods=["POST"])
def register():
    data = request.form
    tasks = {
        'streetNo': data.get('streetNo'),
        'streetName': data.get('streetName'),
        'city': data.get('city'),
        'region': data.get('region'),
        'countryCode': data.get('countryCode'),
        'postalCode': data.get('postalCode')
    }
    tasks_user = {
        'firstName': data.get('firstName'),
        'lastName': data.get('lastName'),
        'phone': data.get('phone'),
        'email': data.get('email')
    }
    res = d_service.update_address("UserResource", "Address", tasks)
    addressID = res[0]['ID']
    print(addressID)
    tasks_user['addressID'] = addressID
    print(tasks_user)
    res = d_service.update_users("UserResource", "User", tasks_user)
    print(res)

    # response = app.response_class(
    #     response=json.dumps(res),
    #     status=201,
    #     mimetype="application/json"
    # )
    rsp = Response(json.dumps(res), status=201, content_type="application/json")
    return rsp

@app.route('/getPorfile', methods=["GET"])
def getProfileInfo():
    user_id = request.args.get('user_id')
    userInfo = "http://usersmicroservice-env.eba-2dzdt4iv.us-east-2.elasticbeanstalk.com/api/users?user_id="+user_id
    print(userInfo)
    mealCreated = "http://3.16.13.44:5001/api/creator_create_which_meal?creator_id="+user_id
    print(mealCreated)
    mealParticipate = "http://3.16.13.44:5001/api/participant_take_which_meal?participant_id="+user_id
    print(mealParticipate)
    url= [
        userInfo,
        mealCreated,
        mealParticipate
    ]

    rs = (grequests.get(u) for u in url)
    x = grequests.map(rs)
    print(x)

    result = dict()
    for i in range(3):
        if i == 0:
            result["user_info"] = x[i].json()[0]
        elif i == 1:
            result["meal_created"] = x[i].json()[0]
        else:
            meal_id = x[i].json()[0]["meals_id"]
            url = ["http://3.16.13.44:5001/api/meals?meal_id=" + str(meal_id)]
            rs1 = (grequests.get(u) for u in url)
            x1 = grequests.map(rs1)
            result["participate_meal"] = x1[0].json()[0]
    print(result)
    rsp = Response(json.dumps(result), status=200, content_type="application/json")
    return rsp

# @app.route('/updateAddress', methods=["POST"])
# def updateAddress():
#     data = request.form
#     tasks = {
#         'ID': data.get('addressID'),
#         'streetNo': data.get('streetNo'),
#         'streetName': data.get('streetName'),
#         'city': data.get('city'),
#         'region': data.get('region'),
#         'countryCode': data.get('countryCode'),
#         'postalCode': data.get('postalCode')
#     }
#
#     if tasks["ID"] is None or tasks["streetNo"] is None or tasks["streetName"] is None or tasks[
#         "city"] is None or tasks["region"] is None or tasks["countryCode"] is None or tasks["postalCode"] is None:
#         rsp = Response(json.dumps(None), status=400, content_type="application/json")
#     else:
#         res = d_service.update_address("UserResource", "Address", tasks)
#         rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
#     return rsp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
