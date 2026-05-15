CREATE DATABASE student_records_db;

USE student_records_db;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    major VARCHAR(100),
    gpa DECIMAL(3,2)
);