from fastapi import HTTPException
from database import cursor, connection


def get_all_users():
    cursor.execute(
        "select * from users"
    )
    return cursor.fetchall()


def get_user_by_id(user_id: int):
    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (user_id,)
    )
    user = cursor.fetchone()
    if not user:
        raise HTTPException(
                status_code = 404,
                detail="User not found"
        )      
    return user

def get_user_details_by_id(user_id: int):

    query = """
    SELECT
        u.id,
        u.name,
        u.email,
        u.age,
        u.phone,
        u.gender,
        u.address,
        u.city,
        u.state,
        u.country,
        u.pincode,

        e.degree,
        e.college_name,
        e.specialization,
        e.passing_year,
        e.percentage,

        p.father_name,
        p.mother_name,
        p.date_of_birth,
        p.marital_status,
        p.nationality,
        p.blood_group,
        p.emergency_contact,
        p.alternate_email

    FROM users u

    LEFT JOIN education e
    ON u.id=e.user_id

    LEFT JOIN personal_details p
    ON u.id=p.user_id

    WHERE u.id=%s
    """

    cursor.execute(query, (user_id,))

    row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return row


def get_all_user_details():

    query = """
    SELECT
        u.id,
        u.name,
        u.email,
        u.age,
        u.phone,
        u.gender,
        u.address,
        u.city,
        u.state,
        u.country,
        u.pincode,

        e.degree,
        e.college_name,
        e.specialization,
        e.passing_year,
        e.percentage,

        p.father_name,
        p.mother_name,
        p.date_of_birth,
        p.marital_status,
        p.nationality,
        p.blood_group,
        p.emergency_contact,
        p.alternate_email

    FROM users u

    LEFT JOIN education e
    ON u.id=e.user_id

    LEFT JOIN personal_details p
    ON u.id=p.user_id
    """

    cursor.execute(query)

    return cursor.fetchall()


def replace_user(user_id: int, user):

    query = """
    UPDATE users
    SET
        name=%s,
        email=%s,
        age=%s,
        phone=%s,
        gender=%s,
        address=%s,
        city=%s,
        state=%s,
        country=%s,
        pincode=%s
    WHERE id=%s
    """

    values = (
        user.name,
        user.email,
        user.age,
        user.phone,
        user.gender,
        user.address,
        user.city,
        user.state,
        user.country,
        user.pincode,
        user_id
    )

    cursor.execute(query, values)
    connection.commit()
    

def get_all_user_details():

    query = """
    SELECT
        u.id,
        u.name,
        u.email,
        u.age,
        u.phone,
        u.gender,
        u.address,
        u.city,
        u.state,
        u.country,
        u.pincode,

        e.degree,
        e.college_name,
        e.specialization,
        e.passing_year,
        e.percentage,

        p.father_name,
        p.mother_name,
        p.date_of_birth,
        p.marital_status,
        p.nationality,
        p.blood_group,
        p.emergency_contact,
        p.alternate_email

    FROM users u

    LEFT JOIN education e
    ON u.id=e.user_id

    LEFT JOIN personal_details p
    ON u.id=p.user_id
    """

    cursor.execute(query)

    return cursor.fetchall()



def update_user(user_id: int, data: dict):
    if not data:
        return
    query = "UPDATE users SET "
    query += ", ".join(
        [f"{field}=%s" for field in data]
    )
    query += " WHERE id=%s"

    values = list(data.values())
    values.append(user_id)

    cursor.execute(
        query,
        tuple(values)
    )
    connection.commit()
    

def delete_user(user_id: int):
    cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
    )
    connection.commit()