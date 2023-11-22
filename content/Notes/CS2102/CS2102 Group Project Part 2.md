### Group 46
---

```sql
CREATE TABLE Educator ( 
	staff_nr VARCHAR(5) PRIMARY KEY, 
	first_name VARCHAR(64) NOT NULL, 
	last_name VARCHAR(64) NOT NULL, 
	email VARCHAR(64) UNIQUE NOT NULL 
); 


CREATE TABLE Student ( 
	student_nr VARCHAR(10) PRIMARY KEY, 
	first_name VARCHAR(64) NOT NULL, 
	last_name VARCHAR(64) NOT NULL, 
	email VARCHAR(64) UNIQUE NOT NULL, 
	last_active TIMESTAMP 
);

CREATE TABLE Groups ( 
	code TEXT PRIMARY KEY, 
	name VARCHAR(64) UNIQUE NOT NULL, 
	description TEXT 
);

CREATE TABLE Tag ( 
	text VARCHAR(64) PRIMARY KEY 
); 

CREATE TABLE Question ( 
	question_id INT PRIMARY KEY, 
	statement TEXT NOT NULL, 
	description TEXT, 
	type VARCHAR(3) NOT NULL CHECK (type = 'MCQ' OR type = 'MRQ'), --either MCQ or MRQ 
	status VARCHAR(7) NOT NULL CHECK (status = 'PRIVATE' OR status = 'PUBLIC'), -- either private or public 
	valid bool NOT NULL, 
	staff_nr VARCHAR(5) NOT NULL, 
	CONSTRAINT fk_staff FOREIGN KEY (staff_nr) REFERENCES Educator(staff_nr) ON UPDATE CASCADE ON DELETE CASCADE 
);
 
CREATE TABLE labels ( 
	question_id INT NOT NULL, 
	tag_text VARCHAR(64) NOT NULL, 
	CONSTRAINT pk_labels PRIMARY KEY (question_id, tag_text), 
	CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES Question (question_id) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT fk_tag_text FOREIGN KEY (tag_text) REFERENCES Tag (text) ON UPDATE CASCADE ON DELETE CASCADE 
);

CREATE TABLE Quiz ( 
	staff_nr INT NOT NULL, 
	quiz_id INT PRIMARY KEY, 
	name VARCHAR(64) NOT NULL, 
	published bool NOT NULL DEFAULT false, 
	max_attempts INT NOT NULL DEFAULT 1, 
	total_points INT, 
	avail_from TIMESTAMP DEFAULT NOW(), --can change to null 
	avail_to TIMESTAMP DEFAULT 'INFINITY', --can change to null 
	time_limit interval, 
	mandatory bool NOT NULL, 
	status VARCHAR(7) NOT NULL, --either public or private 
	CONSTRAINT fk_staff FOREIGN KEY (staff_nr) REFERENCES Educator (staff_nr) ON UPDATE CASCADE ON DELETE CASCADE
);
 
CREATE TABLE contains ( 
	question_id INT, 
	quiz_id INT, 
	mandatory bool NOT NULL, 
	position INT NOT NULL, 
	points INT NOT NULL DEFAULT 0 CHECK (points >= 0), 
	CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES Question (question_id) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT fk_quiz_id FOREIGN KEY (quiz_id) REFERENCES Quiz(quiz_id) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT pk_contains PRIMARY KEY (question_id, quiz_id)
);
 
CREATE TABLE Answer ( 
	answer_id INT NOT NULL, 
	content TEXT NOT NULL,  
	position INT NOT NULL, 
	correct bool NOT NULL, 
	question_id INT NOT NULL, 
	CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES Question (question_id) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT pk_answer PRIMARY KEY (question_id, answer_id) 
); 

CREATE TABLE assigned_to ( 
	quiz_id INT NOT NULL, 
	group_code TEXT NOT NULL, 
	CONSTRAINT fk_quiz_id FOREIGN KEY (quiz_id) REFERENCES Quiz (quiz_id) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT fk_group_code FOREIGN KEY (group_code) REFERENCES Groups (code) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT pk_assigned_to PRIMARY KEY (quiz_id, group_code) 
); 
 
CREATE TABLE member_of ( 
	group_code TEXT NOT NULL, 
	student_nr INT NOT NULL, 
	CONSTRAINT fk_group FOREIGN KEY (group_code) REFERENCES Groups (code), 
	CONSTRAINT fk_student_nr FOREIGN KEY (student_nr) REFERENCES student (student_nr) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT pk_member_of PRIMARY KEY (group_code, student_nr) 
); 
 
CREATE TABLE Submission ( 
	submission_id INT PRIMARY KEY, 
	attempt INT, 
	quiz_id INT NOT NULL, 
	student_nr INT NOT NULL, 
	CONSTRAINT fk_student_nr FOREIGN KEY (student_nr) REFERENCES student (student_nr) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT fk_quiz_id FOREIGN KEY (quiz_id) REFERENCES Quiz(quiz_id) ON UPDATE CASCADE ON DELETE CASCADE 
); 
 
CREATE TABLE part_of ( 
	submission_id INT NOT NULL, 
	answer_id INT NOT NULL, 
	question_id INT NOT NULL, 
	CONSTRAINT fk_submission_id FOREIGN KEY (submission_id) REFERENCES Submission(submission_id) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT fk_answer FOREIGN KEY (answer_id, question_id) REFERENCES Answer(answer_id, question_id) ON UPDATE CASCADE ON DELETE CASCADE, 
	CONSTRAINT pk_part_of PRIMARY KEY (submission_id, answer_id, question_id) 
); 
```
