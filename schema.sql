drop table if exists users;
create table users(
	user_id INTEGER primary key,
	user_firstname TEXT,
	user_lastname TEXT,
	user_gender TEXT
);

drop table if exists scores;
create table scores(
	id INTEGER primary key AUTOINCREMENT,
	user_id INTEGER,
	qid INTEGER,
	answer TEXT,
	score INTEGER,
	r_time TEXT
);

drop table if exists questions;
create table questions(
	id INTEGER primary key AUTOINCREMENT,
	user_id INTEGER,
	qid INTEGER,
	r_time TEXT
);

drop table if exists user_conversation;
create table user_conversation(
	user INTEGER primary key,
	user_firstname TEXT,
	user_lastname TEXT,
	user_gender TEXT,
	user_total_score INTEGER,
	user_history TEXT
)