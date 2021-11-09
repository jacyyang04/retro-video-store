from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, jsonify, make_response, request, abort

# BLUEPRINT
customers_bp = Blueprint("customers_bp", __name__, url_prefix = "/customers")


# HELPER FUNCTIONS
def validate_int(customer_id, param_type):
    try:
        number = int(customer_id)
    except:
        abort(make_response({"message": f"{param_type} needs to be an integer."}, 400))

def get_customer_data_with_id(customer_id):
    validate_int(customer_id, "id")
    customer = Customer.query.get(customer_id)

    if customer is None:
        abort(make_response({"message": f"Customer {customer_id} was not found"}, 404))

    return customer


# GENERAL CUSTOMER ROUTES
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customer_data = []

    customers = Customer.query.all()
    for customer in customers:
        customer_data.append(customer.to_dict())

    return jsonify(customer_data)

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if request_body == None:
        return make_response("You much include name, phone and postcode in order to add customer data.", 404)

    if "name" not in request_body:
        return make_response({"details":"Request body must include name."}, 400)
    elif "phone" not in request_body:
        return make_response({"details":"Request body must include phone."}, 400)
    elif "postal_code" not in request_body:
        return make_response({"details":"Request body must include postal_code."}, 400)

    new_customer = Customer(
        name = request_body["name"],
        phone = request_body["phone"],
        postal_code = request_body["postal_code"]
    )
    
    db.session.add(new_customer)
    db.session.commit()

    return jsonify(new_customer.to_dict()), 201


# CUSTOMER_ID ROUTES
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = get_customer_data_with_id(customer_id)

    return jsonify(customer.to_dict())


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_one_customer(customer_id):
    request_body = request.get_json()
    customer = get_customer_data_with_id(customer_id)

    if request_body == None:
        return make_response("You much include name, phone and postcode in order to add customer data.", 404)

    if "name" not in request_body:
        return make_response({"details":"Request body must include name."}, 400)
    elif "phone" not in request_body:
        return make_response({"details":"Request body must include phone."}, 400)
    elif "postal_code" not in request_body:
        return make_response({"details":"Request body must include postal_code."}, 400)


    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]

    db.session.commit()

    return jsonify(customer.to_dict())


# DELETE ROUTE
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = get_customer_data_with_id(customer_id)

    db.session.delete(customer)
    db.session.commit()

    return make_response({"id": customer.id}, 200)


# CUSTOMER RENTAL ROUTE
@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_videos_checked_out(customer_id):
    customer = get_customer_data_with_id(customer_id)
    
    video_list = []
    video_query = Video.query.filter_by(id=customer_id)

    for video in video_query:
        video_list.append(video.to_dict())
    
    return jsonify(video_list)
