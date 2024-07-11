from flask import Blueprint
from controllers.auth.authentication import register, login
from controllers.user.UserAnalysis import oneCompanyAnalysis, twoCompaniesAnalysis
from controllers.user.PriceAnalysis import plot_prices
from middleware.middleware import token_required

user_routes = Blueprint('user_routes', __name__)

table = 'users'

@user_routes.route('/api/user/login', methods=['POST'])
def UserLogin():
    return login(table)

@user_routes.route('/api/user/register', methods=['POST'])
def UserRegister():
    return register(table)

@user_routes.route('/api/user/one-company-analysis', methods=['GET'])
@token_required
def oneCompany():
    return oneCompanyAnalysis()

@user_routes.route('/api/user/two-companies-analysis', methods=['GET'])
@token_required
def twoCompanies():
    return twoCompaniesAnalysis()

@user_routes.route('/api/user/closing-prices', methods=['POST'])
@token_required
def compareClosePrice():
    return plot_prices('Close')

@user_routes.route('/api/user/opening-prices', methods=['POST'])
@token_required
def compareOpenPrice():
    return plot_prices('Open')

@user_routes.route('/api/user/high-prices', methods=['POST'])
@token_required
def CompareHighPrices():
    return plot_prices('High')

@user_routes.route('/api/user/low-prices', methods=['POST'])
@token_required
def CompareLowPrices():
    return plot_prices('Low')