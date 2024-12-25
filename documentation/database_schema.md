
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
-- tlsa_user table
CREATE TABLE tlsa_user (
    user_id VARCHAR(10) PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254),
    role VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20),
    profile_picture VARCHAR(100),
    real_name VARCHAR(150),
    department VARCHAR(50)
);

-- notice table
CREATE TABLE notice (
    id SERIAL PRIMARY KEY,
    class_or_lab_id INTEGER NOT NULL,
    sender_id VARCHAR(10) NOT NULL REFERENCES tlsa_user(user_id) ON DELETE CASCADE,
    notice_type VARCHAR(10) NOT NULL,
    post_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- notice_completion table
CREATE TABLE notice_completion (
    id SERIAL PRIMARY KEY,
    notice_id INTEGER NOT NULL REFERENCES notice(id) ON DELETE CASCADE,
    user_id VARCHAR(10) NOT NULL REFERENCES tlsa_user(user_id) ON DELETE CASCADE,
    completion_time TIMESTAMP WITH TIME ZONE NOT NULL
);

-- notice_content table
CREATE TABLE notice_content (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(10) NOT NULL,
    text_content TEXT,
    image_content VARCHAR(100),
    file_content VARCHAR(100)
);

-- notice_tag table
CREATE TABLE notice_tag (
    id SERIAL PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

-- notice_content_tag table
CREATE TABLE notice_content_tag (
    notice_content_id INTEGER NOT NULL REFERENCES notice_content(id) ON DELETE CASCADE,
    notice_tag_id INTEGER NOT NULL REFERENCES notice_tag(id) ON DELETE CASCADE,
    PRIMARY KEY (notice_content_id, notice_tag_id)
);

-- notice_row table
CREATE TABLE notice_row (
    id SERIAL PRIMARY KEY,
    notice_id INTEGER NOT NULL REFERENCES notice(id) ON DELETE CASCADE,
    notice_content_id INTEGER NOT NULL REFERENCES notice_content(id) ON DELETE CASCADE,
    order_num INTEGER NOT NULL,
    UNIQUE (notice_id, notice_content_id)
);

-- lab table
CREATE TABLE lab (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(255) NOT NULL,
    safety_equipments TEXT[] DEFAULT ARRAY[]::TEXT[],
    safety_notes TEXT,
    lab_image VARCHAR(100),
    map_image VARCHAR(100)
);

-- manage_lab table
CREATE TABLE manage_lab (
    manager_user_id VARCHAR(10) NOT NULL REFERENCES tlsa_user(user_id) ON DELETE CASCADE,
    lab_id INTEGER NOT NULL REFERENCES lab(id) ON DELETE CASCADE,
    PRIMARY KEY (manager_user_id, lab_id)
);

-- course table
CREATE TABLE course (
    course_code VARCHAR(8) NOT NULL,
    course_sequence VARCHAR(5) NOT NULL,
    department VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (course_code, course_sequence)
);

-- course_enrollment table
CREATE TABLE course_enrollment (
    student_user_id VARCHAR(10) NOT NULL REFERENCES tlsa_user(user_id) ON DELETE CASCADE,
    course_code VARCHAR(8) NOT NULL,
    course_sequence VARCHAR(5) NOT NULL,
    PRIMARY KEY (student_user_id, course_code, course_sequence),
    FOREIGN KEY (course_code, course_sequence) REFERENCES course(course_code, course_sequence) ON DELETE CASCADE
);

-- course_class table
CREATE TABLE course_class (
    course_code VARCHAR(8) NOT NULL,
    course_sequence VARCHAR(5) NOT NULL,
    class_id INTEGER NOT NULL REFERENCES class(id) ON DELETE CASCADE,
    PRIMARY KEY (course_code, course_sequence, class_id),
    FOREIGN KEY (course_code, course_sequence) REFERENCES course(course_code, course_sequence) ON DELETE CASCADE
);

-- class table
CREATE TABLE class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- class_location table
CREATE TABLE class_location (
    class_id INTEGER NOT NULL REFERENCES class(id) ON DELETE CASCADE,
    lab_id INTEGER NOT NULL REFERENCES lab(id) ON DELETE CASCADE,
    PRIMARY KEY (class_id, lab_id)
);

-- teach_class table
CREATE TABLE teach_class (
    class_id INTEGER NOT NULL REFERENCES class(id) ON DELETE CASCADE,
    teacher_id VARCHAR(10) NOT NULL REFERENCES tlsa_user(user_id) ON DELETE CASCADE,
    PRIMARY KEY (class_id, teacher_id)
);

-- class_comment table
CREATE TABLE class_comment (
    id SERIAL PRIMARY KEY,
    sender_id VARCHAR(10) NOT NULL REFERENCES tlsa_user(user_id) ON DELETE CASCADE,
    class_id INTEGER NOT NULL REFERENCES class(id) ON DELETE CASCADE,
    sent_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL
);

-- experiment table
CREATE TABLE experiment (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    estimated_time FLOAT NOT NULL,
    safety_tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    experiment_method_tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    submission_type_tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    other_tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    description TEXT,
    class_id INTEGER NOT NULL REFERENCES class(id) ON DELETE CASCADE
);

-- experiment_image table
CREATE TABLE experiment_image (
    id SERIAL PRIMARY KEY,
    experiment_id INTEGER NOT NULL REFERENCES experiment(id) ON DELETE CASCADE,
    image VARCHAR(100) NOT NULL
);

-- experiment_file table
CREATE TABLE experiment_file (
    id SERIAL PRIMARY KEY,
    experiment_id INTEGER NOT NULL REFERENCES experiment(id) ON DELETE CASCADE,
    file VARCHAR(100) NOT NULL
);
```
