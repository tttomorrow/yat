-- @testpoint: 插入时，使用and列
drop table if exists student_tb1;
create table student_tb1 ("and" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into student_tb1("and") values('zhangsan');
drop table if exists student_tb1;