## TLSA REST API

### Table Of Contents
- [1. User Management](#1-user-management)
- [2. Lab Management](#2-lab-management)
- [3. Course Management](#3-course-management)
- [4. Class Management](#4-class-management)
- [5. Notice Management](#5-notice-management)
- [6. Other Utils](#6-other-utils)

### 1. **User Management**
**Register Student**
- **URL**: `POST /api/v1/users/register`
- **Request JSON**:
    ```json
    {
        "id": "2021000000",
        "name": "name",
        "password": "password",
        "email": "e@mail.com",
        "role": "student"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Student created successfully.",
        "user": {
            "id": "2021000000",
            "name": "name",
            "email": "e@mail.com",
            "role": "student",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    }
    ```

- **URL**: `GET /api/v1/users/user-info?user_id=1`
- Query params:
    - user_id
- Permissions:
    - If student, can only view personal info, cannot view info of other students
    - If teacher or manager, then can view all personal info
- **Response JSON**:
    ```json
    {
        "id": 1,
        "username": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "student"
    }
    ```

**Login User**
- **URL**: `POST /api/v1/users/login`
- **Request JSON**:
    ```json
    {
        "name": "name",
        "password": "password"
    }
    ```
- **Response JSON**:
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
---

### 2. **Lab Management**

**Create Lab**
- **URL**: `POST /api/v1/labs/lab`
- **Request JSON**:
    ```json
    {
        "name": "Organic Chemistry Lab Room 1",
        "location": "Chemistry Building"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Lab created successfully.",
        "lab": {
            "lab_id": 1,
            "name": "Organic Chemistry Lab Room 1",
            "location": "Chemistry Building"
        }
    }
    ```

**Get Lab**
- **URL**: `GET /api/v1/labs/lab?lab_id=1&lab_name=Organic%20Chemistry%20Lab%20Room%201`
- Query params:
    - lab_id
    - lab_name (similarity)
- **Response JSON**:
    ```json
    [
        {
            "lab_id": 1,
            "name": "Organic Chemistry Lab Room 1",
            "location": "Chemistry Building"
        },
        {
            "lab_id": 2,
            "name": "Organic Chemistry Lab Room 1",
            "location": "New Chemistry Building"
        }
    ]
    ```

**Add Lab Manager**
- **URL**: `POST /api/v1/labs/managers`
- **Request JSON**:
    ```json
    {
        "manager_id": "2021000000",
        "lab_id": 1
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Manager added to lab successfully.",
        "manager": {
            "manager_id": "2021000000",
            "lab_id": 1
        }
    }
    ```

**Get Managers for a Lab**
- **URL**: `GET /api/v1/labs/managers?lab_id=1&manager_name=chem`
- Query params:
    - lab_id
    - manager_name (similarity)
- **Response JSON**:
    ```json
    [
        {
            "manager_id": 4,
            "manager_name": "chem1",
            "manager_email": "",
            "lab_id": 1
        },
        {
            "manager_id": 5,
            "manager_name": "chem2",
            "manager_email": "",
            "lab_id": 1
        }
    ]
    ```
---

### 3. **Course Management**

**Create Course**
- **URL**: `POST /api/v1/courses/course`
- **Request JSON**:
    ```json
    {
        "name": "Biology 101"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Course created successfully.",
        "course": {
            "id": 1,
            "name": "Biology 101"
        }
    }
    ```

**Get Course**
- **URL**: `GET /api/v1/courses/course?course_id=1&course_name=Chemistry&personal=false`
- Query params:
    - course_id
    - course_name (similarity)
    - personal (boolean)
- **Response JSON**:
    ```json
    [
        {
        "id": 1,
        "name": "Biology 101"
        }
    ]
    ```

**Enroll Students in Course**
- **URL**: `POST /api/v1/courses/enroll`
- **Request JSON**:
    ```json
    {
        "student_ids": [1, 2],
        "course_id": 1
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Students enrolled successfully.",
        "enrollment": {
            "student_ids": [1, 2],
            "course_id": 1
        }
    }
    ```

**Add Class to Course**
- **URL**: `POST /api/v1/courses/classes`
- **Request JSON**:
    ```json
    {
        "class_id": 1,
        "course_id": 1
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Class added to course successfully.",
        "course_class": {
            "class_id": 1,
            "course_id": 1
        }
    }
    ```

---

### 4. **Class Management**

**Create Class**
- **URL**: `POST /api/v1/classes/class`
- **Request JSON**:
    ```json
    {
        "name": "Biology Lecture",
        "start_time": "2024-01-01T09:00:00Z"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Class created successfully.",
        "class": {
            "id": 1,
            "name": "Biology Lecture",
            "start_time": "2024-01-01T09:00:00Z"
        }
    }
    ```

**Get Class**
- **URL**: `GET /api/v1/classes/class?class_id=1&class_name=Biology&course_id=1`
- Query params:
    - class_id
    - class_name (similarity)
    - course_id
- **Response JSON**:
    ```json
    [
        {
            "id": 1,
            "name": "Biology Lecture",
            "start_time": "2024-01-01T09:00:00Z"
        },
        {
            "id": 2,
            "name": "Chemistry Lab",
            "start_time": "2024-01-02T10:00:00Z"
        }
    ]
    ```

**Assign Teacher to Class**
- **URL**: `POST /api/v1/classes/teachers`
- **Request JSON**:
    ```json
    {
        "class_id": 1,
        "teacher_id": "2021000001"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Teacher assigned to class successfully.",
        "assignment": {
            "class_id": 1,
            "teacher_id": "2021000001"
        }
    }
    ```

**Get All Teachers of a class**
- **URL**: `GET /api/v1/classes/teachers?class_id=1&class_name=Biology`
- Query params:
    - class_id
    - class_name (similarity)
- **Response JSON**:
    ```json
    [
        {
            "class_id": 1,
            "teacher_id": 1
        },
        {
            "class_id": 1,
            "teacher_id": 2
        }
    ]
    ```

**Specify Class Location**
- **URL**: `POST /api/v1/classes/locations`
- **Request JSON**:
    ```json
    {
        "class_id": 1,
        "lab_id": 1
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Location assigned to class successfully.",
        "location": {
            "class_id": 1,
            "lab_id": 1
        }
    }
    ```

**Get All Locations of a class**
- **URL**: `GET /api/v1/classes/locations?class_id=1`
- Query params:
    - class_id
    - class_name (similarity)
- **Response JSON**:
    ```json
    [
        {
            "class_id": 1,
            "lab_id": 1
        },
        {
            "class_id": 1,
            "lab_id": 2
        }
    ]
    ```

**Add Comment to Class**
- **URL**: `POST /api/v1/classes/comments`
- **Request JSON**:
    ```json
    {
        "class_id": 1,
        "content": "Great class!"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Comment added successfully.",
        "comment": {
            "sender_id": "2021000000",
            "class_id": 1,
            "content": "Great class!"
        }
    }
    ```

**Get All Comments of a class**
- **URL**: `GET /api/v1/classes/comments?class_id=1&sender_id=1`
- Query params:
    - class_id
    - sender_id
- **Response JSON**:
    ```json
    [
        {
            "class_id": 1,
            "sender_id": 1,
            "content": "Great class!"
        },
        {
            "class_id": 1,
            "sender_id": 2,
            "content": "yea I agree"
        }
    ]
    ```

---

### 5. **Notice Management**

**Create Notice**
- **URL**: `POST /api/v1/notices/notice`
- **Request JSON**:
    ```json
    {
        "class_or_lab_id": 1,
        "sender_id": "2021000000",
        "notice_type": "class",
        "post_time": "2024-01-01T08:00:00Z",
        "end_time": "2024-01-10T08:00:00Z"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Notice created successfully.",
        "notice": {
            "id": 1,
            "class_or_lab_id": 1,
            "sender_id": "2021000000",
            "notice_type": "class",
            "post_time": "2024-01-01T08:00:00Z",
            "end_time": "2024-01-10T08:00:00Z"
        }
    }
    ```

**Get Notice**
- **URL**: `GET /api/v1/notices/notice?id=1`
- Query params:
    - notice_id
    - sender_id
    - notice_type ("class"|"lab")
- **Response JSON**:
    ```json
    [
        {
            "id": 1,
            "class_or_lab_id": 1,
            "sender_id": "2021000000",
            "notice_type": "class",
            "post_time": "2024-01-01T08:00:00Z",
            "end_time": "2024-01-10T08:00:00Z"
        },
        {
            "id": 2,
            "class_or_lab_id": 2,
            "sender_id": "2021000001",
            "notice_type": "lab",
            "post_time": "2024-01-02T08:00:00Z",
            "end_time": "2024-01-12T08:00:00Z"
        }
    ]
    ```

**Complete Notice**
- **URL**: `POST /api/v1/notices/completion`
- **Request JSON**:
    ```json
    {
        "notice_id": 1,
        "user_id": "2021000000",
        "completion_time": "2024-01-05T08:00:00Z"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Notice marked as completed successfully.",
        "completion": {
            "notice_id": 1,
            "user_id": "2021000000",
            "completion_time": "2024-01-05T08:00:00Z"
        }
    }
    ```

**Create Notice Content**
- **URL**: `POST /api/v1/notices/content`
- **Request JSON**:
    ```json
    {
        "content": "This is a notice content.",
        "content_type": "text"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Notice content created successfully.",
        "content": {
            "id": 1,
            "content": "This is a notice content.",
            "content_type": "text"
        }
    }
    ```

**Create Notice Tag**
- **URL**: `POST /api/v1/notices/tags`
- **Request JSON**:
    ```json
    {
        "tag_name": "Flammable"
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Notice tag created successfully.",
        "tag": {
            "id": 1,
            "tag_name": "Flammable"
        }
    }
    ```

**Link Notice Content and Tag**
- **URL**: `POST /api/v1/notices/content-tags`
- **Request JSON**:
    ```json
    {
        "notice_content_id": 1,
        "notice_tag_id": 1
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Notice content linked to tag successfully.",
        "link": {
            "notice_content_id": 1,
            "notice_tag_id": 1
        }
    }
    ```

**Add Notice Row**
- **URL**: `POST /api/v1/notices/rows`
- **Request JSON**:
    ```json
    {
        "notice_id": 1,
        "notice_content_id": 1,
        "order_num": 1
    }
    ```
- **Response JSON**:
    ```json
    {
        "message": "Notice row added successfully.",
        "row": {
            "notice_id": 1,
            "notice_content_id": 1,
            "order_num": 1
        }
    }
    ```
---

### 6. Other Utils

**Refresh JWT Token**
- **URL**: `POST /api/v1/refresh-token`
- **Request JSON**:
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTIxNzQ1OCwiaWF0IjoxNzMxMTMxMDU4LCJqdGkiOiJmMzE0NDI0NTNlNjE0ODRiOTU2NzNhYzY2NzljNGQ5NiIsInVzZXJfaWQiOjF9.-ZJPvpwsnaGCKrOynhpzHR42ToXBOaY8U65n5I1FoGE",
    }
    ```
- **Response JSON**:
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTIxNzQ1OCwiaWF0IjoxNzMxMTMxMDU4LCJqdGkiOiJmMzE0NDI0NTNlNjE0ODRiOTU2NzNhYzY2NzljNGQ5NiIsInVzZXJfaWQiOjF9.-ZJPvpwsnaGCKrOynhpzHR42ToXBOaY8U65n5I1FoGE",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxMTMxMzU4LCJpYXQiOjE3MzExMzEwNTgsImp0aSI6ImMwNDRjMjgxOWY0YjQ0OTFhMTc3MTQ2YjI4MWVhZjY4IiwidXNlcl9pZCI6MX0.8NjXmkWDho9fGxIMbDNb7JhRdDAAvJPWkuDWuJF4ORo"
    }
    ```