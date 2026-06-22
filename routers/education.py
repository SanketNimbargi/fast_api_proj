from fastapi import APIRouter, Depends, HTTPException
from database import cursor, connection
from schemas.education_schema import Education, UpdateEducation
from auth import verify_token, get_current_user

router = APIRouter(
    prefix="/education",
    tags=["Education"],
    dependencies=[Depends(verify_token)]
)


@router.post("")
def create_education(
        education: Education,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    query = """
    INSERT INTO education
    (
        user_id,
        degree,
        college_name,
        specialization,
        passing_year,
        percentage
    )
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    values = (
        user_id,
        education.degree,
        education.college_name,
        education.specialization,
        education.passing_year,
        education.percentage
    )

    cursor.execute(query, values)
    connection.commit()

    return {
        "message": "Education added successfully",
        "education_id": cursor.lastrowid
    }



@router.get("")
def get_my_education(
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    query = """
    SELECT *
    FROM education
    WHERE user_id=%s
    """

    cursor.execute(query, (user_id,))
    records = cursor.fetchall()

    result = []

    for row in records:
        result.append({
            "edu_id": row[0],
            "user_id": row[1],
            "degree": row[2],
            "college_name": row[3],
            "specialization": row[4],
            "passing_year": row[5],
            "percentage": row[6]
        })

    return result



@router.get("/{edu_id}")
def get_education(
        edu_id: int,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    query = """
    SELECT *
    FROM education
    WHERE edu_id=%s
    AND user_id=%s
    """

    cursor.execute(query, (edu_id, user_id))

    row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Education record not found"
        )

    return {
        "edu_id": row[0],
        "user_id": row[1],
        "degree": row[2],
        "college_name": row[3],
        "specialization": row[4],
        "passing_year": row[5],
        "percentage": row[6]
    }


@router.put("/{edu_id}")
def update_education(
        edu_id: int,
        education: Education,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    cursor.execute(
        """
        SELECT *
        FROM education
        WHERE edu_id=%s
        AND user_id=%s
        """,
        (edu_id, user_id)
    )

    record = cursor.fetchone()

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    query = """
    UPDATE education
    SET
        degree=%s,
        college_name=%s,
        specialization=%s,
        passing_year=%s,
        percentage=%s
    WHERE edu_id=%s
    """

    values = (
        education.degree,
        education.college_name,
        education.specialization,
        education.passing_year,
        education.percentage,
        edu_id
    )

    cursor.execute(query, values)
    connection.commit()

    return {
        "message": "Education updated successfully"
    }


@router.patch("/{edu_id}")
def patch_education(
        edu_id: int,
        education: UpdateEducation,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    cursor.execute(
        """
        SELECT *
        FROM education
        WHERE edu_id=%s
        AND user_id=%s
        """,
        (edu_id, user_id)
    )

    record = cursor.fetchone()

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    query = "UPDATE education SET "
    values = []

    if education.degree is not None:
        query += "degree=%s,"
        values.append(education.degree)

    if education.college_name is not None:
        query += "college_name=%s,"
        values.append(education.college_name)

    if education.specialization is not None:
        query += "specialization=%s,"
        values.append(education.specialization)

    if education.passing_year is not None:
        query += "passing_year=%s,"
        values.append(education.passing_year)

    if education.percentage is not None:
        query += "percentage=%s,"
        values.append(education.percentage)

    if len(values) == 0:
        return {
            "message": "No fields provided"
        }

    query = query.rstrip(",")
    query += " WHERE edu_id=%s"

    values.append(edu_id)

    cursor.execute(query, tuple(values))
    connection.commit()

    return {
        "message": "Education updated successfully"
    }



@router.delete("/{edu_id}")
def delete_education(
        edu_id: int,
        current_user=Depends(get_current_user)):

    user_id = current_user[0]

    cursor.execute(
        """
        SELECT *
        FROM education
        WHERE edu_id=%s
        AND user_id=%s
        """,
        (edu_id, user_id)
    )

    record = cursor.fetchone()

    if not record:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    cursor.execute(
        """
        DELETE FROM education
        WHERE edu_id=%s
        """,
        (edu_id,)
    )

    connection.commit()

    return {
        "message": "Education deleted successfully"
    }

















# from fastapi import APIRouter, Depends
# from database import cursor, connection
# from schemas.education_schema import Education, UpdateEducation
# from auth import verify_token

# router = APIRouter(
#     prefix="/education",
#     tags=["education"],
#     dependencies=[Depends(verify_token)]
# )


# @router.post("")
# def create_education(education: Education):
#     query = """
#     INSERT INTO education
#     (user_id, degree, college_name, specialization, passing_year, percentage)
#     VALUES (%s, %s, %s, %s, %s, %s)
#     """

#     values = (
#         education.user_id,
#         education.degree,
#         education.college_name,
#         education.specialization,
#         education.passing_year,
#         education.percentage
#     )

#     cursor.execute(query, values)
#     connection.commit()

#     return {
#         "message": "Education added successfully",
#         "education_id": cursor.lastrowid
#     }


# @router.get("")
# def get_all_education():
#     cursor.execute("SELECT * FROM education")
#     records = cursor.fetchall()
#     education_list = []

#     for edu in records:
#         education_list.append({
#             "edu_id": edu[0],
#             "user_id": edu[1],
#             "degree": edu[2],
#             "college_name": edu[3],
#             "specialization": edu[4],
#             "passing_year": edu[5],
#             "percentage": edu[6]
#         })

#     return education_list


# @router.get("/{user_id}")
# def get_education(user_id: int):
#     query = "SELECT * FROM education WHERE user_id=%s"
#     cursor.execute(query, (user_id,))
#     records = cursor.fetchall()

#     education_list = []

#     for edu in records:
#         education_list.append({
#             "edu_id": edu[0],
#             "user_id": edu[1],
#             "degree": edu[2],
#             "college_name": edu[3],
#             "specialization": edu[4],
#             "passing_year": edu[5],
#             "percentage": edu[6]
#         })

#     return education_list


# @router.get("/{user_id}/details")
# def get_user_details(user_id: int):
#     query = """
#     SELECT
#         u.id,
#         u.name,
#         u.email,
#         u.phone,
#         e.edu_id,
#         e.degree,
#         e.college_name,
#         e.specialization,
#         e.passing_year,
#         e.percentage
#     FROM users u
#     JOIN education e
#     ON u.id = e.user_id
#     WHERE u.id = %s
#     """

#     cursor.execute(query, (user_id,))
#     records = cursor.fetchall()

#     result = []

#     for row in records:
#         result.append({
#             "user_id": row[0],
#             "name": row[1],
#             "email": row[2],
#             "phone": row[3],
#             "education_id": row[4],
#             "degree": row[5],
#             "college_name": row[6],
#             "specialization": row[7],
#             "passing_year": row[8],
#             "percentage": row[9]
#         })

#     return result


# @router.put("/{edu_id}")
# def update_education(edu_id: int, education: Education):
#     query = """
#     UPDATE education
#     SET
#         user_id=%s,
#         degree=%s,
#         college_name=%s,
#         specialization=%s,
#         passing_year=%s,
#         percentage=%s
#     WHERE edu_id=%s
#     """

#     values = (
#         education.user_id,
#         education.degree,
#         education.college_name,
#         education.specialization,
#         education.passing_year,
#         education.percentage,
#         edu_id
#     )

#     cursor.execute(query, values)
#     connection.commit()

#     return {"message": "Education updated successfully"}


# @router.patch("/{edu_id}")
# def patch_education(edu_id: int, education: UpdateEducation):
#     query = "UPDATE education SET "
#     values = []

#     if education.degree is not None:
#         query += "degree=%s, "
#         values.append(education.degree)

#     if education.college_name is not None:
#         query += "college_name=%s, "
#         values.append(education.college_name)

#     if education.specialization is not None:
#         query += "specialization=%s, "
#         values.append(education.specialization)

#     if education.passing_year is not None:
#         query += "passing_year=%s, "
#         values.append(education.passing_year)

#     if education.percentage is not None:
#         query += "percentage=%s, "
#         values.append(education.percentage)

#     if not values:
#         return {"message": "No fields provided"}

#     query = query.rstrip(", ")
#     query += " WHERE edu_id=%s"
#     values.append(edu_id)

#     cursor.execute(query, tuple(values))
#     connection.commit()

#     return {"message": "Education updated successfully"}


# @router.delete("/{edu_id}")
# def delete_education(edu_id: int):
#     query = "DELETE FROM education WHERE edu_id=%s"
#     cursor.execute(query, (edu_id,))
#     connection.commit()

#     if cursor.rowcount == 0:
#         return {"message": "Education record not found"}

#     return {"message": "Education deleted successfully"}