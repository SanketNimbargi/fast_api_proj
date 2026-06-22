def education_to_dict(row):

    return {
        "edu_id": row[0],
        "user_id": row[1],
        "degree": row[2],
        "college_name": row[3],
        "specialization": row[4],
        "passing_year": row[5],
        "percentage": row[6]
    }