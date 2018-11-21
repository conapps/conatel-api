from src import db

class Ap(db.Model):
    __tablename__='aps'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ap_mac = db.Column(db.String(200), unique=True, nullable=False)
    location_name = db.Column(db.String(200), unique=False, nullable=True)
    has_licence = db.Column(db.Boolean, unique=False)

    def json(self):
        return {'ap_mac': self.ap_mac, 'location_name': self.location_name, 'has_licence': self.has_licence}

    def add_ap(_ap_mac, _location_name, _has_licence):
        new_ap = Ap(ap_mac=_ap_mac, location_name=_location_name,
                    has_licence=_has_licence)
        db.session.add(new_ap)
        db.session.commit()

    def get_all_aps():
        return [Ap.json(ap) for ap in Ap.query.all()]

    def get_ap(_ap_mac):
        ap = Ap.query.filter_by(ap_mac=_ap_mac).first()
        return Ap.json(ap)

    def delete_ap(_ap_mac):
        Ap.query.filter_by(ap_mac=_ap_mac).delete()
        db.session.commit()

    def update_ap(_ap_mac, ap_update):
        ap_to_update = Ap.query.filter_by(ap_mac=_ap_mac).first()
        if 'location_name' in ap_update:
            ap_to_update.location_name = ap_update['location_name']
        if 'has_licence' in ap_update:
            ap_to_update.has_licence = ap_update['has_licence']
        db.session.commit()
