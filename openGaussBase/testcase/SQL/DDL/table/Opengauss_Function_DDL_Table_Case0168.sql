-- @testpoint: 创建列存表（ 组合索引）
drop table if exists table_1;
drop table if exists table_2;
DROP INDEX if exists table_index;
create table table_1(id int,sname char(20),city varchar(20),number number)with (ORIENTATION=COLUMN);
select * from table_1;

create table table_2(id int,sname char(20),course varchar(20),score number)with (ORIENTATION=COLUMN);
insert into table_2 values(1,'joe','english',123);
insert into table_2 values(2,'jojo','math',124);
insert into table_2 values(3,'jane','history',85);
select * from table_2;
create index table_index on table_1(id,sname);
select * from table_1 as t1,table_2 as t2 where t1.id=t2.id and t1.sname=t2.sname;
DROP INDEX if exists table_index;
drop table if exists table_1;
drop table if exists table_2;