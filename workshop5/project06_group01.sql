-- task 1
with all_rental as (
   select count(rental_id) / count(distinct customer_id) as average_all
     from rental
), cte as (
  select customer_id, count(rental_id) as cnt
  from rental
  group by customer_id
  having count(rental_id) > (
    select * from all_rental
  )
)

select a.customer_id, b.first_name, b.last_name, a.cnt
from cte a
join customer b
on a.customer_id = b.customer_id

-- task 2
CREATE TABLE product_logs (
    log_id INT PRIMARY KEY,
    log_detail VARCHAR(100),
    story_point INT,
    priority INT
);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    dummy_name VARCHAR(50),
    job_role VARCHAR(50),
    log_id INT,
    FOREIGN KEY (log_id) REFERENCES product_logs(log_id)
);

CREATE TABLE sub_tasks (
    subtask_id INT PRIMARY KEY,
    task_detail VARCHAR(100),
    hours_needed INT,
    log_id INT,
    FOREIGN KEY (log_id) REFERENCES product_logs(log_id)
);

CREATE TABLE sprint_meetings (
    meeting_id INT PRIMARY KEY,
    duration INT,
    meeting_date DATE,
    student_id INT,
    subtask_id INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subtask_id) REFERENCES sub_tasks(subtask_id)
);

CREATE TABLE student_subtasks (
    student_id INT,
    subtask_id INT,
    PRIMARY KEY (student_id, subtask_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subtask_id) REFERENCES sub_tasks(subtask_id)
);

CREATE TABLE meeting_attendees (
    meeting_id INT,
    student_id INT,
    PRIMARY KEY (meeting_id, student_id),
    FOREIGN KEY (meeting_id) REFERENCES sprint_meetings(meeting_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE meeting_subtasks (
    meeting_id INT,
    subtask_id INT,
    PRIMARY KEY (meeting_id, subtask_id),
    FOREIGN KEY (meeting_id) REFERENCES sprint_meetings(meeting_id),
    FOREIGN KEY (subtask_id) REFERENCES sub_tasks(subtask_id)
);

INSERT INTO product_logs (log_id, log_detail, story_point, priority)
VALUES
    (1, 'testing', 1, 1),
    (2, 'testing2', 2, 2);

INSERT INTO students (student_id, dummy_name, job_role, log_id)
VALUES
    (1, 'Alice Chen', 'Frontend Developer', 1),
    (2, 'Bob Martinez', 'Backend Developer', 1),
    (3, 'Carol Singh', 'Database Administrator', 2),
    (4, 'David Thompson', 'Full Stack Developer', 2);

INSERT INTO sub_tasks (subtask_id, task_detail, hours_needed, log_id)
VALUES
    (1, 'Design UI mockups', 8, 1),
    (2, 'Implement responsive layout', 12, 1),
    (3, 'Add form validation', 6, 1),
    (4, 'Set up database schema', 10, 2),
    (5, 'Create API endpoints', 15, 2),
    (6, 'Write unit tests', 8, 2);

INSERT INTO sprint_meetings (meeting_id, duration, meeting_date, student_id, subtask_id)
VALUES
    (1, 1, '2026-01-29', 1, 1),
    (2, 1, '2026-03-12', 2, 2),
    (3, 1, '2026-04-09', 3, 3);

SELECT 
    s.dummy_name,
    p.log_detail,
    st.task_detail,
    sm.meeting_date
FROM students s
JOIN product_logs p ON s.log_id = p.log_id
JOIN sub_tasks st ON st.log_id = p.log_id
JOIN student_subtasks ss ON ss.student_id = s.student_id AND ss.subtask_id = st.subtask_id
JOIN meeting_attendees ma ON ma.student_id = s.student_id
JOIN sprint_meetings sm ON sm.meeting_id = ma.meeting_id;
