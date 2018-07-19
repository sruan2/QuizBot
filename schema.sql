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


drop table if exists user;
create table user(
	user_id bigint primary key,
	user_firstname TEXT,
	user_lastname TEXT,
	user_status INTEGER,
	reg_time TEXT
);

drop table if exists conversation;
create table conversation(
	id INTEGER primary key AUTO_INCREMENT,
	user_id bigint,
	dialog TEXT,
	type TEXT,
	subject TEXT,
	timestamp TEXT,
	qid INTEGER,
	score INTEGER
);

