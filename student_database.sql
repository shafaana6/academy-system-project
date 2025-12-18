CREATE DATABASE academy_system;
USE academy_system;

CREATE TABLE learners (
    learner_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100),
    email_address VARCHAR(100),
    course_name VARCHAR(50),
    year_of_study INT
);
CREATE TABLE grades (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    learner_id INT,
    subject_name VARCHAR(50),
    score INT,
    FOREIGN KEY (learner_id) REFERENCES learners(learner_id)
);
