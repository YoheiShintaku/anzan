-- local
-- create database anzan
-- use anzan
CREATE TABLE log (
  user_id int,
  t datetime,
  digit int,
  intervalSec float,
  len int,
  ans int,
  correct int,
  judge int
);

-- heroku
CREATE TABLE log (
  user_id integer,
  t timestamp,
  digit integer,
  intervalSec float,
  len integer,
  ans integer,
  correct integer,
  judge integer
);
