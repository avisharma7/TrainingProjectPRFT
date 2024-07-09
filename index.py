from flask import Flask

# Import and register the user routes blueprint
from routes.userRoutes import user_routes
from routes.companyRoutes import company_routes

app = Flask(__name__)

app.register_blueprint(user_routes)
app.register_blueprint(company_routes)

if __name__ == '__main__':
    app.run(debug=True)
