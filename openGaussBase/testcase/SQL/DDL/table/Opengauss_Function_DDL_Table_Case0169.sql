-- @testpoint: 创建列存表以及btree索引
drop table if exists table_1;
DROP INDEX if exists table_1_index1;
create table table_1(id int,sname char(20),city varchar(20),number number)with (ORIENTATION=COLUMN);
insert into table_1 values(1,'joe','a',12323455646);
insert into table_1 values(2,'jojo','b',124232345456);
insert into table_1 values(3,'jane','c',12557676878);
CREATE INDEX table_1_index1 ON table_1 USING btree(id);
DROP INDEX if exists table_index;
drop table if exists table_1;