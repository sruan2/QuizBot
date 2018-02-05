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