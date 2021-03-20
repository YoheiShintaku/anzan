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
-- d7d7jfml0mg7e7
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

CREATE TABLE users (
  user_id integer,
  name varchar,
  pass varchar,
  created timestamp,
  updated timestamp
);
ALTER TABLE users ADD PRIMARY KEY(user_id);

CREATE TABLE setting (
  user_id integer,
  len integer,
  intervalSec float,
  digit1 integer,
  digit1_rate float,
  auto boolean,
  improve varchar,
  updated timestamp
);
ALTER TABLE setting ADD PRIMARY KEY(user_id);
