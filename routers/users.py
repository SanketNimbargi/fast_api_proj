from fastapi import APIRouter, Depends, HTTPException
from database import cursor, connection
from schemas.user_schema import User, UpdateUser
from auth import verify_token, get_current_user
from services.users_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
    replace_user,
    get_all_user_details,
    get_user_details_by_id
)
from utils.user_details_mapper import user_details_to_dict
from utils.user_mapper import user_to_dict



router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_token)]
)

@router.get("")
def get_users():
    
    users = get_all_users()
    return [
        user_to_dict(user)
        for user in users
    ]


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    
    return user_to_dict(current_user)



@router.get("/{id}")
def get_user(id: int):
    
    user = get_user_by_id(id)
    return user_to_dict(user)



@router.get("/details/all")
def get_all_user_details():

    rows = get_all_user_details()
    return [
        user_details_to_dict(row)
        for row in rows
    ]



@router.get("/{id}/details")
def get_user_details(id: int):

    row = get_user_details_by_id(id)
    return user_details_to_dict(row)



@router.put("/me")
def update_me(
        user: User,
        current_user=Depends(get_current_user)):

    replace_user(
        current_user[0],
        user
    )
    return {
        "message": "Profile updated successfully"
    }



@router.patch("/me")
def patch_me(
        user: UpdateUser,
        current_user=Depends(get_current_user)):
    
    data = user.model_dump(
        exclude_none=True
    )
    
    if not data:
        return {
            "message": "No fields provided"
        }
    update_user(
        current_user[0],
        data
    )
    return {
        "message": "Profile updated successfully"
    }

   
@router.delete("/me")
def delete_me(current_user=Depends(get_current_user)):
    
    delete_user(
        current_user[0]
    )
    return {
        "message": "Account deleted successfully"
    }

   

























# from fastapi import APIRouter, Depends, HTTPException

# from database import cursor, connection
# from schemas.user_schema import User, UpdateUser
# from auth import get_current_user

# router = APIRouter(
#     prefix="/users",
#     tags=["Users"]
# )


# @router.post("")
# def create_user(user: User):
#     query = """
#     INSERT INTO users
#     (name, email, age, phone, gender, address, city, state, country, pincode)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """

#     values = (
#         user.name,
#         user.email,
#         user.age,
#         user.phone,
#         user.gender,
#         user.address,
#         user.city,
#         user.state,
#         user.country,
#         user.pincode
#     )

#     cursor.execute(query, values)
#     connection.commit()

#     return {
#         "message": "User created successfully",
#         "id": cursor.lastrowid
#     }


# @router.get("")
# def get_users():
#     cursor.execute("SELECT * FROM users")
#     records = cursor.fetchall()
#     users = []

#     for user in records:
#         users.append({
#             "id": user[0],
#             "name": user[1],
#             "email": user[2],
#             "age": user[3],
#             "phone": user[4],
#             "gender": user[5],
#             "address": user[6],
#             "city": user[7],
#             "state": user[8],
#             "country": user[9],
#             "pincode": user[10]
#         })

#     return users


# @router.get("/details/all")
# def get_all_user_details():
#     query = """
#     SELECT
#         u.id,
#         u.name,
#         u.email,
#         u.age,
#         u.phone,
#         u.gender,
#         u.address,
#         u.city,
#         u.state,
#         u.country,
#         u.pincode,

#         e.degree,
#         e.college_name,
#         e.specialization,
#         e.passing_year,
#         e.percentage,

#         p.father_name,
#         p.mother_name,
#         p.date_of_birth,
#         p.marital_status,
#         p.nationality,
#         p.blood_group,
#         p.emergency_contact,
#         p.alternate_email

#     FROM users u

#     LEFT JOIN education e
#     ON u.id = e.user_id

#     LEFT JOIN personal_details p
#     ON u.id = p.user_id
#     """

#     cursor.execute(query)
#     records = cursor.fetchall()
#     users = []

#     for row in records:
#         users.append({
#             "id": row[0],
#             "name": row[1],
#             "email": row[2],
#             "age": row[3],
#             "phone": row[4],
#             "gender": row[5],
#             "address": row[6],
#             "city": row[7],
#             "state": row[8],
#             "country": row[9],
#             "pincode": row[10],
#             "degree": row[11],
#             "college_name": row[12],
#             "specialization": row[13],
#             "passing_year": row[14],
#             "percentage": row[15],
#             "father_name": row[16],
#             "mother_name": row[17],
#             "date_of_birth": row[18],
#             "marital_status": row[19],
#             "nationality": row[20],
#             "blood_group": row[21],
#             "emergency_contact": row[22],
#             "alternate_email": row[23]
#         })

#     return users


# @router.get("/{id}")
# def get_user(id: int):
#     query = "SELECT * FROM users WHERE id=%s"
#     cursor.execute(query, (id,))
#     user = cursor.fetchone()

#     if user:
#         return {
#             "id": user[0],
#             "name": user[1],
#             "email": user[2],
#             "age": user[3],
#             "phone": user[4],
#             "gender": user[5],
#             "address": user[6],
#             "city": user[7],
#             "state": user[8],
#             "country": user[9],
#             "pincode": user[10]
#         }

#     return {"message": "User not found"}


# @router.get("/{id}/details")
# def get_user_details(id: int):
#     query = """
#     SELECT
#         u.id,
#         u.name,
#         u.email,
#         u.age,
#         u.phone,
#         u.gender,
#         u.address,
#         u.city,
#         u.state,
#         u.country,
#         u.pincode,

#         e.degree,
#         e.college_name,
#         e.specialization,
#         e.passing_year,
#         e.percentage,

#         p.father_name,
#         p.mother_name,
#         p.date_of_birth,
#         p.marital_status,
#         p.nationality,
#         p.blood_group,
#         p.emergency_contact,
#         p.alternate_email

#     FROM users u

#     LEFT JOIN education e
#     ON u.id = e.user_id

#     LEFT JOIN personal_details p
#     ON u.id = p.user_id

#     WHERE u.id = %s
#     """

#     cursor.execute(query, (id,))
#     result = cursor.fetchone()
#     return result


# @router.put("/{id}")
# def update_user(id: int, user: User):
#     query = """
#     UPDATE users
#     SET
#     name=%s,
#     email=%s,
#     age=%s,
#     phone=%s,
#     gender=%s,
#     address=%s,
#     city=%s,
#     state=%s,
#     country=%s,
#     pincode=%s
#     WHERE id=%s
#     """

#     values = (
#         user.name,
#         user.email,
#         user.age,
#         user.phone,
#         user.gender,
#         user.address,
#         user.city,
#         user.state,
#         user.country,
#         user.pincode,
#         id
#     )

#     cursor.execute(query, values)
#     connection.commit()

#     return {"message": "User updated successfully"}


# @router.patch("/{id}")
# def patch_user(id: int, user: UpdateUser):
#     query = "UPDATE users SET "
#     values = []

#     if user.name is not None:
#         query += "name=%s, "
#         values.append(user.name)

#     if user.email is not None:
#         query += "email=%s, "
#         values.append(user.email)

#     if user.age is not None:
#         query += "age=%s, "
#         values.append(user.age)

#     if user.phone is not None:
#         query += "phone=%s, "
#         values.append(user.phone)

#     if user.gender is not None:
#         query += "gender=%s, "
#         values.append(user.gender)

#     if user.address is not None:
#         query += "address=%s, "
#         values.append(user.address)

#     if user.city is not None:
#         query += "city=%s, "
#         values.append(user.city)

#     if user.state is not None:
#         query += "state=%s, "
#         values.append(user.state)

#     if user.country is not None:
#         query += "country=%s, "
#         values.append(user.country)

#     if user.pincode is not None:
#         query += "pincode=%s, "
#         values.append(user.pincode)

#     if not values:
#         return {"message": "No fields provided"}

#     query = query.rstrip(", ")
#     query += " WHERE id=%s"
#     values.append(id)

#     cursor.execute(query, tuple(values))
#     connection.commit()

#     return {"message": "User updated successfully"}


# @router.delete("/{id}")
# def delete_user(id: int):
#     query = "DELETE FROM users WHERE id=%s"
#     cursor.execute(query, (id,))
#     connection.commit()

#     if cursor.rowcount == 0:
#         return {"message": "User not found"}

#     return {"message": "User deleted successfully"}