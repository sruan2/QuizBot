drop table if exists user_score;
create table user_score (
  user_id INTEGER primary key,
  user_firstname TEXT,
  user_lastname TEXT,
  user_gender TEXT,
  score REAL
);
