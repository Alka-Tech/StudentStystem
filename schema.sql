DROP TABLE IF EXISTS students;

CREATE TABLE students (
    ID INTEGER PRIMARY KEY,
    LastName TEXT NOT NULL,
    FirstName TEXT NOT NULL,
    City TEXT,
    State TEXT,
    Gender TEXT,
    StudentStatus TEXT,
    Major TEXT,
    Country TEXT, 
    Age TEXT,
    SAT TEXT,
    Grade TEXT,
    Height TEXT
);