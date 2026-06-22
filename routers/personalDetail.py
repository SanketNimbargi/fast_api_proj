from fastapi import APIRouter, Depends, HTTPException
from database import cursor, connection
from schemas.personalDetail_schema import (
    PersonalDetails,
    UpdatePersonalDetails
)
from auth import verify_token, get_current_user
from services.personal_details_service import (
    create_personal_details_record,
    get_personal_details_by_user,
    get_personal_details_by_id,
    replace_personal_details,
    patch_personal_details,
    delete_personal_details_record
)
from utils.personal_details_mapper import (
    personal_details_to_dict
)




router = APIRouter(
    prefix="/personal-details",
    tags=["Personal Details"],
    dependencies=[Depends(verify_token)]
)


@router.post("")
def create_personal_details(
        details: PersonalDetails,
        current_user=Depends(get_current_user)):

    record_id = create_personal_details_record(
        current_user[0],
        details
    )
    return {
        "message": "Personal details added successfully",
        "id": record_id
    }


@router.get("")
def get_personal_details(
        current_user=Depends(get_current_user)):

    row = get_personal_details_by_user(
        current_user[0]
    )
    return personal_details_to_dict(row)


@router.get("/{id}")
def get_personal_detail(
        id: int,
        current_user=Depends(get_current_user)):

    row = get_personal_details_by_id(
        id,
        current_user[0]
    )
    return personal_details_to_dict(row)


@router.put("/{id}")
def update_personal_details(
        id: int,
        personal: PersonalDetails,
        current_user=Depends(get_current_user)):

    get_personal_details_by_id(
        id,
        current_user[0]
    )
    replace_personal_details(
        id,
        personal
    )
    return {
        "message": "Personal details updated successfully"
    }
    


@router.patch("/{id}")
def patch_personal_details(
        id: int,
        personal: UpdatePersonalDetails,
        current_user=Depends(get_current_user)):

    get_personal_details_by_id(
        id,
        current_user[0]
    )
    data = personal.model_dump(
        exclude_none=True
    )
    if not data:
        return {
            "message": "No fields provided"
        }
    patch_personal_details(
        id,
        data
    )
    return {
        "message": "Personal details updated successfully"
    }


@router.delete("/{id}")
def delete_personal_details(
        id: int,
        current_user=Depends(get_current_user)):

    get_personal_details_by_id(
        id,
        current_user[0]
    )
    delete_personal_details_record(
        id
    )
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