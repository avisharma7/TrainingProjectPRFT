from flask import Blueprint
from controllers.user.userAuth import user_login, user_register
from controllers.user.UserAnalysis import oneCompanyAnalysis, twoCompaniesAnalysis
from middleware.middleware import token_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/user/login', methods=['POST'])
def login():
    return user_login()

@user_routes.route('/api/user/register', methods=['POST'])
def register():
    return user_register()

@user_routes.route('/api/user/one-company-analysis', methods=['GET'])
@token_required
def oneCompany():
    return oneCompanyAnalysis()

@user_routes.route('/api/user/two-companies-analysis', methods=['GET'])
@token_required
def twoCompanies():
    return twoCompaniesAnalysis()