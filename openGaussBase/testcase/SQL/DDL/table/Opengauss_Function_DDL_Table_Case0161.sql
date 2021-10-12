-- @testpoint: 创建带普通索引的表

drop table if exists table_t1;
 CREATE TABLE table_t1
(SM_SK           INTEGER               NOT NULL,
 SM_id        CHAR(16)              NOT NULL,
 SM_TYPE         CHAR(30)
 );
DROP INDEX if exists table_t1_index1;
CREATE UNIQUE INDEX table_t1_index1 ON table_t1(SM_SK);
insert into table_t1 values(1,'a','1a'),(2,'b','2b'),(3,'c','3c');
DROP INDEX if exists table_t1_index1;
drop table if exists table_t1;