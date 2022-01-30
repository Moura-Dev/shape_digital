import logging
from statistics import mean

from flask import Blueprint, jsonify, request

from apis.models.cost import equipment_cost
from apis.models.equipment import equipment
from apis.models.model import db
from apis.models.vessel import vessel

healthcheck_blueprint = Blueprint("healthcheck", __name__)
vessels_blueprint = Blueprint("vessels", __name__)
equipments_blueprint = Blueprint("equipments", __name__)


@healthcheck_blueprint.route("/", methods=["GET"])
def healthcheck():
    """Checks if the system is alive
    ---
    responses:
      200:
        description: OK if the system is alive
    """
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger.info("Test the health of the system")
    return "OK", 200


@vessels_blueprint.route("/insert_vessel", methods=["POST"])
def insert_vessel():
    """Insert a new vessel
    ---
    parameters:
        - name: code
          in: body
          type: string
          required: true
    responses:
      201:
        description: OK
      400:
        description: ERROR
      409:
        description: FAIL
    """
    try:
        logging.basicConfig(
            format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger(__name__)
        logger.info("insert_vessel endpoint")
        request_json = request.get_json()
        code = request_json.get("code")

        if not code:
            return {"message": "Code Required"}, 400

        exists = vessel.query.filter(vessel.code == code).first()

        if exists:
            return {"message": "Vessel already exists"}, 409

        new_vessel = vessel(code=code)
        db.session.add(new_vessel)
        db.session.commit()
        return {"message": "OK"}, 201

    except:
        return {"message": "Error"}, 400


@equipments_blueprint.route("/insert_equipment_cost", methods=["POST"])
def insert_cost():
    """inser_cost
    ---
    parameters:
        - name: code
          in: body
          type: string
          required: true
        - name: type
          in: body
          type: string
          required: true
        - name: cost
          in: body
          type: string
          required: true
    responses:
      201:
        description: returns OK if the equipment was correctly inserted
      400:
        description: Error
    """
    try:
        logging.basicConfig(
            format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger(__name__)
        logger.info("Runing")
        request_json = request.get_json()

        code = request_json.get("code")
        type_ = request_json.get("type")
        cost = request_json.get("cost")
        new_cost = equipment_cost(equipment_code=code, type_=type_, cost=cost)
        db.session.add(new_cost)
        db.session.commit()
        return {"message": "OK"}, 201

    except:
        return {"message": "Error"}, 400


@equipments_blueprint.route("/insert_equipment", methods=["POST"])
def insert_equipment():
    """insert_equipment
    ---
    parameters:
        - name: vessel_code
          in: body
          type: string
          required: true
        - name: code
          in: body
          type: string
          required: true
        - name: name
          in: body
          type: string
          required: true
        - name: location
          in: body
          type: string
          required: true
    responses:
      201:
        description: returns OK if the equipment was correctly inserted
      400:
        description: Error
      409:
        description: Equipment already exists

    """
    try:
        logging.basicConfig(
            format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger(__name__)
        logger.info("Runing")
        request_json = request.get_json()

        name = request_json.get("name")
        code = request_json.get("code")
        location = request_json.get("location")
        vessel_id = request_json.get("vessel_id")
        exists = equipment.query.filter(equipment.code == code).first()
        if exists:
            return {"message": "Equipment already exists"}, 409
        new_equipment = equipment(
            name=name, code=code, location=location, vessel_id=vessel_id
        )
        db.session.add(new_equipment)
        db.session.commit()
        return {"message": "OK"}, 201

    except:
        return {"message": "Error"}, 400


@equipments_blueprint.route("/update_equipment_status", methods=["PUT"])
def update_equipment_status():
    """update_equipment_status
    ---
    parameters:
        - name: code
          in: body
          type: string
          required: true
    responses:
      201:
        description: returns OK if the equipments were correctly updated
      400:
        description: Error
    """
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger.info("Runing")
    try:
        data = request.args
        codes = data.get("code")
        list_codes = codes.split(",")
        for n in list_codes:
            query = equipment.query.filter(equipment.code == n).first()

            if query:
                query.active = False

        db.session.commit()

        return {"message": "OK"}, 201

    except:
        return {"message": "Error"}, 400


@equipments_blueprint.route("/active_equipments", methods=["GET"])
def active_equipment():
    """active_equipments
    ---
    parameters:
        - name: vessel_code
          in: query
          type: string
          required: true
    responses:
      200:
        description: returns a json with equipments key and a list of equipments
      400:
        description: error
    """
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger.info("Runing")
    try:
        list_equipments = []
        args = request.args
        code = args.get("code")
        equipments = (
            equipment.query.join(vessel)
            .filter(vessel.code == code, equipment.active == True)
            .all()
        )
        for equip in equipments:
            list_equipments.append(
                {
                    "id": equip.id,
                    "name": equip.name,
                    "code": equip.code,
                    "location": equip.location,
                    "active": equip.active,
                }
            )

        return jsonify(list_equipments)

    except:
        return {"message": "Error"}, 400


@equipments_blueprint.route("/cost", methods=["GET"])
def equipment_cost_total():
    """equipment_cost
    ---
    parameters:
        - name: code
          in: query
          type: string
          required: true
    responses:
      200:
        description: returns a json with cost equipments
      400:
        description: error
    """
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger.info("Runing")
    try:
        costs = []
        args = request.args
        code = args.get("code")
        name = args.get("name")

        if name:
            costs_equipment = (
                equipment_cost.query.join(equipment)
                .filter(equipment.name == name)
                .all()
            )
        else:
            costs_equipment = (
                equipment_cost.query.join(equipment)
                .filter(equipment.code == code)
                .all()
            )

        for x in costs_equipment:
            costs.append(float(x.cost))

        total_cost = sum(costs)

        return jsonify(total_cost)

    except:
        return {"message": "Error"}, 400


@vessels_blueprint.route("/cost", methods=["GET"])
def vessel_cost_average():
    """vessel_cost_average
    ---
    parameters:
        - name: code
          in: query
          type: string
          required: true
    responses:
      200:
        description: returns a json with  vessel cost average
      400:
        description: error
    """
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger.info("Runing")
    try:

        costs = []
        args = request.args
        code = args.get("code")

        average_vessels = (
            equipment_cost.query.join(equipment)
            .join(vessel)
            .filter(vessel.code == code)
            .all()
        )
        for x in average_vessels:
            x = x.cost.replace(",", ".")
            costs.append(float(x))
        average_cost = mean(costs)

        return jsonify(average_cost)
    except:
        return {"message": "Error"}, 400
