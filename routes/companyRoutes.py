from flask import Blueprint
from controllers.company.companyAuth import company_login, company_register

company_routes = Blueprint('company_routes', __name__)

@company_routes.route('/api/company/login', methods=['POST'])
def login():
    return company_login()

@company_routes.route('/api/company/register', methods=['POST'])
def register():
    return company_register()