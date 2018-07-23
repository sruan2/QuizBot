/*
drop table if exists users;
create table users(
	user_id bigint primary key,
	user_firstname TEXT,
	user_lastname TEXT,
	user_gender TEXT,
	user_status INTEGER
);

drop table if exists scores;
create table scores(
	id INTEGER primary key AUTO_INCREMENT,
	user_id bigint,
	qid INTEGER,
	answer TEXT,
	score INTEGER,
	r_time TEXT
);

drop table if exists questions;
create table questions(
	id INTEGER primary key AUTO_INCREMENT,
	user_id bigint,
	qid INTEGER,
	subject TEXT,
	r_time TEXT
);
*/

-- The following three tables are currently being used. The rest tables are deprecated.

drop table if exists user;
create table user(
	user_id bigint primary key,
	user_firstname TEXT,
	user_lastname TEXT,
	reg_time TEXT,
    current_subject TEXT
);


drop table if exists conversation;
create table conversation(
	uid INTEGER primary key AUTO_INCREMENT,
	sender bigint,
	recipient bigint,
	time_stamp TEXT,
    type TEXT,
    dialogue TEXT
);


-- user study history
-- used to store qids, scores, and timestamps
-- and pass to question sequencing models
drop table if exists user_history;
create table user_history(
    user_id bigint,
    qid INTEGER,
    subject TEXT,
    score INTEGER,
    begin_timestamp TEXT,
    end_timestamp TEXT,
    begin_uid INTEGER primary key,
    end_uid INTEGER
);

