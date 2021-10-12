-- @testpoint: 创建列存表，列存表GIN索引设置唯一索引时合理报错
drop table if exists table_t1;
 CREATE TABLE table_t1
(SM_SK           INTEGER               NOT NULL,
 SM_id        CHAR(16)              NOT NULL,
 SM_TYPE         CHAR(30)
 )with (ORIENTATION=COLUMN);
DROP INDEX if exists table_t1_index1;
CREATE UNIQUE INDEX table_t1_index1 ON table_t1 using gin(SM_SK);
insert into table_t1 values (1,'a','1a'),(2,'b','2b'),(3,'c','3c');
DROP INDEX if exists table_t1_index1;
drop table if exists table_t1;

-- @testpoint: 创建列存表以及列存表GIN索引不支持唯一部分索引
drop table if exists table_t2;
 CREATE TABLE table_t2
(SM_SK           INTEGER               NOT NULL,
 SM_id        CHAR(16)              NOT NULL,
 SM_TYPE         CHAR(30)
 )with (ORIENTATION=COLUMN);
DROP INDEX if exists table_t2_index2;
CREATE  INDEX table_t2_index2 ON table_t2 using gin(SM_SK) where SM_SK > 5;
insert into table_t2 values (1,'a','1a'),(2,'b','2b'),(3,'c','3c');
DROP INDEX if exists table_t2_index2;
drop table if exists table_t2;