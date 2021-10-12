-- @testpoint: 定义和使用and列带双引号
drop table if exists student_tb1;
create table student_tb1 ("and" char(20),stu_age int,sex char(10),score int,address char(10));
insert into student_tb1 ("and")values('zhangsan');
select * from student_tb1;
drop table if exists student_tb1;