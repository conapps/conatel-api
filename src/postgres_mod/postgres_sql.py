######
# POSTGRES EXAMPLE WITH CRUD METHODS FOR A ENTITY
######

import psycopg2

db_connection = psycopg2.connect("postgres://conatel:conatelconatel@api-test.c3bx7yer08ph.us-east-1.rds.amazonaws.com/api_test")

def create_tables():
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE aps(
            ap_id text PRIMARY KEY,
            ap_mac TEXT,
            location_name TEXT,
            has_licence boolean
        );
        """
    )
    db_connection.commit()
    cursor.close()


def add_ap(ap_dict):
    cursor = db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO aps (ap_id, ap_mac, location_name, has_licence) VALUES(%s, %s, %s, %s, %s, %s);
        """,
        (
            ap_dict['ap_id'],
            ap_dict['ap_mac'],
            ap_dict['location_name'],
            ap_dict['has_licence']
        )
    )
    db_connection.commit()
    cursor.close()


def delete_ap(ap_id):
    cursor = db_connection.cursor()
    cursor.execute(
        """
        DELETE FROM aps WHERE ap_id=%s;
        """,
        (ap_id,)
    )
    db_connection.commit()
    cursor.close()


def edit_ap(ap_id, ap_dict):
    cursor = db_connection.cursor()
    cursor.execute(
        """
        UPDATE aps SET location_name=%s, ap_mac=%s, has_licence=%s
        WHERE ap_id = %s;
        """,
        (
            ap_dict['location_name'],
            ap_dict['ap_mac'],
            ap_dict['has_licence'],
            ap_id
        )
    )
    db_connection.commit()
    cursor.close()


def get_all_aps():
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM aps;")
    all_aps = cursor.fetchall()
    aps = []
    for raw_ap in all_aps:
        aps.append(serialize_ap(raw_ap))

    return aps


def get_ap(ap_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM aps WHERE ap_id = %s;", (ap_id,))
    raw_ap = cursor.fetchone()

    return serialize_ap(raw_ap)


def serialize_ap(raw_ap):
    return {
        "ap_id": raw_ap[0],
        "ap_mac": raw_ap[1],
        "location_name": raw_ap[2],
        "has_licence": raw_ap[3],
    }
