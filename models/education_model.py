from database import cursor, connection

cursor.execute("""
CREATE TABLE IF NOT EXISTS education(
    edu_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    degree VARCHAR(100),
    college_name VARCHAR(200),
    specialization VARCHAR(100),
    passing_year INT,
    percentage FLOAT,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
)
""")

connection.commit()