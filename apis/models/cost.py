from apis.models.model import db


class equipment_cost(db.Model):
    __tablename__ = "equipment_costs"

    id = db.Column(db.BigInteger, primary_key=True)
    equipment_code = db.Column(db.String(80), db.ForeignKey("equipments.code"))
    type_ = db.Column(db.String(256), nullable=False)
    cost = db.Column(db.String(80))
