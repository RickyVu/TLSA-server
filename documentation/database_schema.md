
### At a glance
![ER-diagram](TLSA%20ER.png)
```
role = ‘student’|’teacher’|’manager’
notice_type = ‘class’|’lab’

user(id, name, password, email, role, created_at, updated_at)
course(id, name)
class(id, name, start_time, created_at, updated_at)
lab(id, name, location)

notice(id, class_or_lab_id, sender_id, notice_type, post_time, end_time, created_at, update_at)
notice_completion(notice_id, user_id, completion_time)
notice_content(id, content, content_type)
notice_tag(id, tag_name)
notice_content_tag(notice_content_id, notice_tag_id)
notice_row(notice_id, notice_content_id, order_num)

manage_lab(manager_id, lab_id)
teach_class(class_id, teacher_id)
course_enrollment(student_id, course_id)
class_location(class_id, lab_id)
course_class(course_id, class_id)
class_comment(sender_id, class_id, sent_time, content)
```
---
### Detailed Schema
```postgres
CREATE TABLE user (
    id VARCHAR(10) PRIMARY KEY, 
    name VARCHAR(50), 
    password VARCHAR(255), 
    email VARCHAR(255) UNIQUE, 
    role ENUM('student', 'teacher', 'manager'), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE course (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100)
);

CREATE TABLE class (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100), 
    start_time TIMESTAMP, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE lab (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100) UNIQUE, 
    location VARCHAR(255)
);

CREATE TABLE notice (
    id SERIAL PRIMARY KEY, 
class_or_lab_id INT,
sender_id VARCHAR(10) REFERENCES user(id), 
    notice_type ENUM('class', 'lab'), 
    post_time TIMESTAMP, 
    end_time TIMESTAMP, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE notice_completion (
    notice_id INT REFERENCES notice(id), 
    user_id VARCHAR(10) REFERENCES user(id), 
    completion_time TIMESTAMP
);

CREATE TABLE notice_content (
    id SERIAL PRIMARY KEY, 
    content TEXT, 
content_type VARCHAR(50)
);

CREATE TABLE notice_tag (
    id SERIAL PRIMARY KEY, 
    tag_name VARCHAR(50) UNIQUE
);

CREATE TABLE notice_content_tag (
    notice_content_id INT REFERENCES notice_content(id), 
    notice_tag_id INT REFERENCES notice_tag(id), 
    PRIMARY KEY (notice_content_id, notice_tag_id)
);

CREATE TABLE notice_row (
    notice_id INT REFERENCES notice(id) ON DELETE CASCADE,
    notice_content_id INT REFERENCES notice_content(id), 
    order_num INT,
    PRIMARY KEY (notice_id, notice_content_id)
);

CREATE TABLE manage_lab (
    manager_id VARCHAR(10) REFERENCES user(id), 
    lab_id INT REFERENCE lab(id)
);

CREATE TABLE teach_class (
    class_id INT REFERENCES class(id), 
    teacher_id VARCHAR(10) REFERENCES user(id)
);

CREATE TABLE course_enrollment (
    student_id VARCHAR(10) REFERENCES user(id), 
    course_id INT REFERENCES course(id)
);

CREATE TABLE class_location (
    class_id INT REFERENCES class(id), 
    lab_id INT REFERENCE lab(id)
);

CREATE TABLE course_class (
    course_id INT REFERENCES course(id), 
    class_id INT REFERENCES class(id)
);

CREATE TABLE class_comment (
    sender_id VARCHAR(10) REFERENCES user(id), 
    class_id INT REFERENCES class(id), 
    sent_time TIMESTAMP, 
    content TEXT
);
```