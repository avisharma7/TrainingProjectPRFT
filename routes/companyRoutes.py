from flask import Blueprint
from auth.authentication import register, login
from controllers.company.CompanyAnalysis import create_data, update_data, delete_data, get_data
from middleware.middleware import token_required

company_routes = Blueprint('company_routes', __name__)

table = 'company'

@company_routes.route('/api/company/login', methods=['POST'])
def CompanyLogin():
    return login(table)

@company_routes.route('/api/company/register', methods=['POST'])
def ComapnyRegister():
    return register(table)

@company_routes.route('/api/company/create', methods=['POST'])
@token_required
def createCompany():
    return create_data()

@company_routes.route('/api/company/read/<company_symbol>', methods=['GET'])
@token_required
def readCompany(company_symbol):
    return get_data(company_symbol)

@company_routes.route('/api/company/update/<company_symbol>', methods=['PUT'])
@token_required
def updateCompany(company_symbol):
    return update_data(company_symbol)

@company_routes.route('/api/company/delete/<company_symbol>', methods=['DELETE'])
@token_required
def deleteCompany(company_symbol):
    return delete_data(company_symbol)
