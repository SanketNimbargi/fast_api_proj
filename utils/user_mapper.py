
def user_to_dict(user):
    return {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "age": user[3],
        "phone": user[4],
        "gender": user[5],
        "address": user[6],
        "city": user[7],
        "state": user[8],
        "country": user[9],
        "pincode": user[10]
    }