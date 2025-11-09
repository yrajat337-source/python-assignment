import psycopg2

try:
    # Connect to your existing 'student' database
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",           # your PostgreSQL username
        password="9816224042@Bs",  # replace with your PostgreSQL password
        database="student"         # your existing database
    )
    cur = conn.cursor()
    print("Connected to 'student' database successfully!")

    # Create Students table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        age INT
    );
    """)

    # Create Courses table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id SERIAL PRIMARY KEY,
        course_name VARCHAR(100) NOT NULL,
        instructor VARCHAR(50)
    );
    """)

    # Create Enrollments table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id SERIAL PRIMARY KEY,
        student_id INT REFERENCES students(student_id),
        course_id INT REFERENCES courses(course_id)
    );
    """)

    conn.commit()
    print("Tables created successfully!")


    # Students
    cur.execute("INSERT INTO students (name, age) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ("Alice", 20))
    cur.execute("INSERT INTO students (name, age) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ("Bob", 22))
    cur.execute("INSERT INTO students (name, age) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ("Charlie", 21))
    
    # Courses
    cur.execute("INSERT INTO courses (course_name, instructor) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ("Math", "Dr. Smith"))
    cur.execute("INSERT INTO courses (course_name, instructor) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ("English", "Prof. Johnson"))
    cur.execute("INSERT INTO courses (course_name, instructor) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ("Science", "Dr. Brown"))
    
    # Enrollments
    cur.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (1, 1))
    cur.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (2, 2))
    cur.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (3, 3))
    
    conn.commit()
    print("Sample data inserted successfully!")
except Exception as e:
    print("Error:", e)



finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Connection closed.")
