-- @testpoint: 创建行存表以及行存表B-tree索支持唯一索引
drop table if exists table_t3;
 CREATE TABLE table_t3
(SM_SK           INTEGER               NOT NULL,
 SM_id        CHAR(16)              NOT NULL,
 SM_TYPE         CHAR(30)
 );
DROP INDEX if exists table_t3_index1;
CREATE UNIQUE INDEX table_t3_index1 ON table_t3 using btree(SM_SK);
insert into table_t3 values (1,'a','1a'),(2,'b','2b'),(3,'c','3c');
DROP INDEX if exists table_t3_index1;
drop table if exists table_t3;
