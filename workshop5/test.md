This database consists of four tables as follows:

students:
student_id (int, Primary Key),

dummy_name (VARCHAR(50)),

job_role (VARCHAR (50)),

log_id (int).

product_logs:
log_id (int, Primary Key),

log_detail (VARCHAR(100)),

story_point (int),

priority (int),

subtask_id (int).

sub_tasks:
subtask_id (int, Primary Key),

task_detail (VARCHAR(100)),

hours_needed (int),

log_id (int),

student_id (int).

sprint_meetings:
meeting_id (int),

duration (int),

meeting_date (date),

student_id (int),

subtask_id (int).

 

Note on relationships (Entity Relationships Diagram, ERD)

A student can be assigned to many subtasks; a subtask can be developed by many students (many-to-many).
A product_log can be divided into many subtasks (one-to-many).
A student can be assigned to one product_log (one-to-one).
A sprint_meeting will discuss many subtasks (one-to-many).
A sprint_meeting will have many students attending (one-to-many).
