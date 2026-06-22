from fastapi import APIRouter, Depends, HTTPException
from database import cursor, connection
from schemas.personalDetail_schema import (
    PersonalDetails,
    UpdatePersonalDetails
)
from auth import verify_token, get_current_user

router = APIRouter(
    prefix="/personal-details",
    tags=["Personal Details"],
    dependencies=[Depends(verify_token)]
)


@router.post("")
def create_personal_details(
        details: PersonalDetails,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

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
    INSERT INTO personal_details
    (
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

    return {
        "message": "Personal details added successfully",
        "id": cursor.lastrowid
    }


@router.get("")
def get_personal_details(
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    query = """
    SELECT *
    FROM personal_details
    WHERE user_id=%s
    """

    cursor.execute(query, (user_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="No personal details found"
        )

    return {
        "id": row[0],
        "user_id": row[1],
        "father_name": row[2],
        "mother_name": row[3],
        "date_of_birth": row[4],
        "marital_status": row[5],
        "nationality": row[6],
        "blood_group": row[7],
        "emergency_contact": row[8],
        "alternate_email": row[9]
    }


@router.get("/{id}")
def get_personal_detail(
        id: int,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    query = """
    SELECT *
    FROM personal_details
    WHERE id=%s
    AND user_id=%s
    """

    cursor.execute(query, (id, user_id))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Personal details not found"
        )

    return {
        "id": row[0],
        "user_id": row[1],
        "father_name": row[2],
        "mother_name": row[3],
        "date_of_birth": row[4],
        "marital_status": row[5],
        "nationality": row[6],
        "blood_group": row[7],
        "emergency_contact": row[8],
        "alternate_email": row[9]
    }


@router.put("/{id}")
def update_personal_details(
        id: int,
        personal: PersonalDetails,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    cursor.execute(
        """
        SELECT *
        FROM personal_details
        WHERE id=%s
        AND user_id=%s
        """,
        (id, user_id)
    )

    record = cursor.fetchone()

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

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

    return {
        "message": "Personal details updated successfully"
    }


@router.patch("/{id}")
def patch_personal_details(
        id: int,
        personal: UpdatePersonalDetails,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    cursor.execute(
        """
        SELECT *
        FROM personal_details
        WHERE id=%s
        AND user_id=%s
        """,
        (id, user_id)
    )

    record = cursor.fetchone()

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    query = "UPDATE personal_details SET "
    values = []

    if personal.father_name is not None:
        query += "father_name=%s,"
        values.append(personal.father_name)

    if personal.mother_name is not None:
        query += "mother_name=%s,"
        values.append(personal.mother_name)

    if personal.date_of_birth is not None:
        query += "date_of_birth=%s,"
        values.append(personal.date_of_birth)

    if personal.marital_status is not None:
        query += "marital_status=%s,"
        values.append(personal.marital_status)

    if personal.nationality is not None:
        query += "nationality=%s,"
        values.append(personal.nationality)

    if personal.blood_group is not None:
        query += "blood_group=%s,"
        values.append(personal.blood_group)

    if personal.emergency_contact is not None:
        query += "emergency_contact=%s,"
        values.append(personal.emergency_contact)

    if personal.alternate_email is not None:
        query += "alternate_email=%s,"
        values.append(personal.alternate_email)

    if len(values) == 0:
        return {
            "message": "No fields provided"
        }

    query = query.rstrip(",")
    query += " WHERE id=%s"

    values.append(id)

    cursor.execute(query, tuple(values))
    connection.commit()

    return {
        "message": "Personal details updated successfully"
    }


@router.delete("/{id}")
def delete_personal_details(
        id: int,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    cursor.execute(
        """
        SELECT *
        FROM personal_details
        WHERE id=%s
        AND user_id=%s
        """,
        (id, user_id)
    )

    record = cursor.fetchone()

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    cursor.execute(
        """
        DELETE FROM personal_details
        WHERE id=%s
        """,
        (id,)
    )

    connection.commit()

    return {
        "message": "Personal details deleted successfully"
    }












# from fastapi import APIRouter, Depends
# from database import cursor, connection
# from schemas.personalDetail_schema import PersonalDetails, UpdatePersonalDetails
# from auth import verify_token

# router = APIRouter(
#     prefix="/personal-details",
#     tags=["personal-details"],
#     dependencies=[Depends(verify_token)]
# )


# @router.post("")
# def add_personal_details(details: PersonalDetails):
#     query = """
#     INSERT INTO personal_details
#     (
#         user_id,
#         father_name,
#         mother_name,
#         date_of_birth,
#         marital_status,
#         nationality,
#         blood_group,
#         emergency_contact,
#         alternate_email
#     )
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """

#     values = (
#         details.user_id,
#         details.father_name,
#         details.mother_name,
#         details.date_of_birth,
#         details.marital_status,
#         details.nationality,
#         details.blood_group,
#         details.emergency_contact,
#         details.alternate_email
#     )

#     cursor.execute(query, values)
#     connection.commit()

#     return {
#         "message": "Personal details added successfully",
#         "id": cursor.lastrowid
#     }


# @router.get("")
# def get_personal_details():
#     cursor.execute("SELECT * FROM personal_details")
#     records = cursor.fetchall()

#     details = []

#     for data in records:
#         details.append({
#             "id": data[0],
#             "user_id": data[1],
#             "father_name": data[2],
#             "mother_name": data[3],
#             "date_of_birth": data[4],
#             "marital_status": data[5],
#             "nationality": data[6],
#             "blood_group": data[7],
#             "emergency_contact": data[8],
#             "alternate_email": data[9]
#         })

#     return details


# @router.get("/{id}")
# def get_personal_detail(id: int):
#     query = "SELECT * FROM personal_details WHERE id=%s"
#     cursor.execute(query, (id,))
#     data = cursor.fetchone()

#     if data:
#         return {
#             "id": data[0],
#             "user_id": data[1],
#             "father_name": data[2],
#             "mother_name": data[3],
#             "date_of_birth": data[4],
#             "marital_status": data[5],
#             "nationality": data[6],
#             "blood_group": data[7],
#             "emergency_contact": data[8],
#             "alternate_email": data[9]
#         }

#     return {"message": "Personal details not found"}


# @router.put("/{id}")
# def update_personal_detail(id: int, personal: PersonalDetails):
#     query = """
#     UPDATE personal_details
#     SET
#         user_id=%s,
#         father_name=%s,
#         mother_name=%s,
#         date_of_birth=%s,
#         marital_status=%s,
#         nationality=%s,
#         blood_group=%s,
#         emergency_contact=%s,
#         alternate_email=%s
#     WHERE id=%s
#     """

#     values = (
#         personal.user_id,
#         personal.father_name,
#         personal.mother_name,
#         personal.date_of_birth,
#         personal.marital_status,
#         personal.nationality,
#         personal.blood_group,
#         personal.emergency_contact,
#         personal.alternate_email,
#         id
#     )

#     cursor.execute(query, values)
#     connection.commit()

#     return {"message": "Personal details updated successfully"}


# @router.patch("/{id}")
# def patch_personal_detail(id: int, personal: UpdatePersonalDetails):
#     query = "UPDATE personal_details SET "
#     values = []

#     if personal.father_name is not None:
#         query += "father_name=%s, "
#         values.append(personal.father_name)

#     if personal.mother_name is not None:
#         query += "mother_name=%s, "
#         values.append(personal.mother_name)

#     if personal.date_of_birth is not None:
#         query += "date_of_birth=%s, "
#         values.append(personal.date_of_birth)

#     if personal.marital_status is not None:
#         query += "marital_status=%s, "
#         values.append(personal.marital_status)

#     if personal.nationality is not None:
#         query += "nationality=%s, "
#         values.append(personal.nationality)

#     if personal.blood_group is not None:
#         query += "blood_group=%s, "
#         values.append(personal.blood_group)

#     if personal.emergency_contact is not None:
#         query += "emergency_contact=%s, "
#         values.append(personal.emergency_contact)

#     if personal.alternate_email is not None:
#         query += "alternate_email=%s, "
#         values.append(personal.alternate_email)

#     if not values:
#         return {"message": "No fields provided"}

#     query = query.rstrip(", ")
#     query += " WHERE id=%s"
#     values.append(id)

#     cursor.execute(query, tuple(values))
#     connection.commit()

#     return {"message": "Personal details updated successfully"}


# @router.delete("/{id}")
# def delete_personal_detail(id: int):
#     query = "DELETE FROM personal_details WHERE id=%s"
#     cursor.execute(query, (id,))
#     connection.commit()

#     if cursor.rowcount == 0:
#         return {"message": "Personal details not found"}

#     return {"message": "Personal details deleted successfully"}