def user_details_to_dict(row):

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "age": row[3],
        "phone": row[4],
        "gender": row[5],
        "address": row[6],
        "city": row[7],
        "state": row[8],
        "country": row[9],
        "pincode": row[10],
        "degree": row[11],
        "college_name": row[12],
        "specialization": row[13],
        "passing_year": row[14],
        "percentage": row[15],
        "father_name": row[16],
        "mother_name": row[17],
        "date_of_birth": row[18],
        "marital_status": row[19],
        "nationality": row[20],
        "blood_group": row[21],
        "emergency_contact": row[22],
        "alternate_email": row[23]
    }