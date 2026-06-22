from fastapi import HTTPException
from database import cursor, connection


def create_personal_details_record(user_id: int, details):

    cursor.execute(
        "SELECT * FROM personal_details WHERE user_id=%s",
        (user_id,)
    )

    existing_record = cursor.fetchone()

    if existing_record:
        raise HTTPException(
            status_code=400,
            detail="Personal details already exist"
        )

    query = """
    INSERT INTO personal_details(
        user_id,
        father_name,
        mother_name,
        date_of_birth,
        marital_status,
        nationality,
        blood_group,
        emergency_contact,
        alternate_email
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        user_id,
        details.father_name,
        details.mother_name,
        details.date_of_birth,
        details.marital_status,
        details.nationality,
        details.blood_group,
        details.emergency_contact,
        details.alternate_email
    )

    cursor.execute(query, values)
    connection.commit()

    return cursor.lastrowid


def get_personal_details_by_id(id: int, user_id: int):

    cursor.execute(
        """
        SELECT *
        FROM personal_details
        WHERE id=%s
        AND user_id=%s
        """,
        (id, user_id)
    )

    row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Personal details not found"
        )

    return row


def get_personal_details_by_user(user_id: int):

    cursor.execute(
        """
        SELECT *
        FROM personal_details
        WHERE user_id=%s
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="No personal details found"
        )

    return row


def replace_personal_details(id: int, personal):

    query = """
    UPDATE personal_details
    SET
        father_name=%s,
        mother_name=%s,
        date_of_birth=%s,
        marital_status=%s,
        nationality=%s,
        blood_group=%s,
        emergency_contact=%s,
        alternate_email=%s
    WHERE id=%s
    """

    values = (
        personal.father_name,
        personal.mother_name,
        personal.date_of_birth,
        personal.marital_status,
        personal.nationality,
        personal.blood_group,
        personal.emergency_contact,
        personal.alternate_email,
        id
    )

    cursor.execute(query, values)
    connection.commit()


def patch_personal_details(id: int, data: dict):

    query = "UPDATE personal_details SET "

    query += ", ".join(
        [f"{field}=%s" for field in data]
    )

    query += " WHERE id=%s"

    values = list(data.values())
    values.append(id)

    cursor.execute(query, tuple(values))
    connection.commit()


def delete_personal_details_record(id: int):

    cursor.execute(
        """
        DELETE FROM personal_details
        WHERE id=%s
        """,
        (id,)
    )

    connection.commit()