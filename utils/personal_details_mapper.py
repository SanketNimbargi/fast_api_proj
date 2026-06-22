def personal_details_to_dict(row):

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