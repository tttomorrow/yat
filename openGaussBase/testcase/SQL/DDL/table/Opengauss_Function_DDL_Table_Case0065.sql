-- @testpoint: create 列存表table 与 with 子句（COMPRESSION,）
DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id                      NUMBER(7),
 use_filename              VARCHAR2(20)
)with(ORIENTATION=COLUMN,COMPRESSION=YES);
drop table if exists tab_12;


DROP TABLE IF EXISTS tab_13;
CREATE TABLE tab_13
(id                      NUMBER(7),
 name              VARCHAR2(20)
  )with(ORIENTATION=COLUMN,COMPRESSION=NO);
DROP TABLE IF EXISTS tab_13;

DROP TABLE IF EXISTS tab_14;
CREATE TABLE tab_14
(id                      NUMBER(7),
 name              VARCHAR2(20)
  )with(ORIENTATION=COLUMN,COMPRESSION=MIDDLE);
DROP TABLE IF EXISTS tab_14;

DROP TABLE IF EXISTS tab_15;
CREATE TABLE tab_15
(id                      NUMBER(7),
 name              VARCHAR2(20)
  )with(ORIENTATION=COLUMN,COMPRESSION=HIGH);
DROP TABLE IF EXISTS tab_15;