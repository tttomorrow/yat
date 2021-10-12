-- @testpoint: 创建列存表以及psort索引
drop table if exists table_2;
DROP INDEX if exists table_index2;
create table table_2(id int,sname char(20),course varchar(20) default 'math',score number)with (ORIENTATION=COLUMN);
insert into table_2 values(1,'joe','english',123);
insert into table_2 (id,sname,score)values(2,'jojo',124);
insert into table_2 values(3,'jane','history',85);
select * from table_2;
create index table_index2 on table_2 USING Psort(course);
drop table if exists table_2;