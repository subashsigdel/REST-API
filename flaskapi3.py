from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Customer Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

# Initialize the database within the app context
with app.app_context():
    db.create_all()

# Customer Resource
class CustomerResource(Resource):
    def get(self):
        customers = Customer.query.all()
        return jsonify([{'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone': customer.phone} for customer in customers])

    def post(self):
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        new_customer = Customer(name=name, email=email, phone=phone)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer added successfully', 'customer': {'id': new_customer.id, 'name': new_customer.name, 'email': new_customer.email, 'phone': new_customer.phone}})

api.add_resource(CustomerResource, '/customers')

# Route to render the template
@app.route('/')
def index():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
