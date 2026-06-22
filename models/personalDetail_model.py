from database import cursor, connection

cursor.execute("""
CREATE TABLE IF NOT EXISTS personal_details(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    date_of_birth DATE,
    marital_status VARCHAR(20),
    nationality VARCHAR(50),
    blood_group VARCHAR(10),
    emergency_contact BIGINT,
    alternate_email VARCHAR(100),

    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

connection.commit()