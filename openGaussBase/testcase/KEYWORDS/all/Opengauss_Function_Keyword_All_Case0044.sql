-- @testpoint: 排序时，使用all列
drop table if exists student_tb1;
create table student_tb1 ("All" char(20),stu_age int,sex char(10),score int,address char(10));
insert into student_tb1 ("All",stu_age)values('zhangsan',20);
insert into student_tb1 ("All",stu_age)values('lisi',25);
select * from student_tb1 order by "All";
drop table if exists student_tb1;