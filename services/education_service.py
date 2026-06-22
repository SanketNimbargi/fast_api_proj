from fastapi import HTTPException
from database import cursor, connection


def create_education_record(user_id: int, education):

    query = """
    INSERT INTO education(
        user_id,
        degree,
        college_name,
        specialization,
        passing_year,
        percentage
    )
    VALUES(%s,%s,%s,%s,%s,%s)
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

    return cursor.lastrowid


def get_all_education(user_id: int):

    cursor.execute(
        """
        SELECT *
        FROM education
        WHERE user_id=%s
        """,
        (user_id,)
    )

    return cursor.fetchall()


def get_education_by_id(edu_id: int, user_id: int):

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
            status_code=404,
            detail="Education record not found"
        )

    return record


def replace_education(edu_id: int, education):

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


def patch_education_record(edu_id: int, data: dict):

    query = "UPDATE education SET "

    query += ", ".join(
        [f"{field}=%s" for field in data]
    )

    query += " WHERE edu_id=%s"

    values = list(data.values())
    values.append(edu_id)

    cursor.execute(query, tuple(values))
    connection.commit()


def delete_education_record(edu_id: int):

    cursor.execute(
        """
        DELETE FROM education
        WHERE edu_id=%s
        """,
        (edu_id,)
    )

    connection.commit()