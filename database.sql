-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS studentdb;

-- Select and use the created database
USE studentdb;

-- Create the students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Auto-incrementing unique identifier for each student
    name VARCHAR(100) NOT NULL,        -- Student's full name
    email VARCHAR(100) NOT NULL,       -- Student's email address
    course VARCHAR(100) NOT NULL       -- Course enrolled by the student
);