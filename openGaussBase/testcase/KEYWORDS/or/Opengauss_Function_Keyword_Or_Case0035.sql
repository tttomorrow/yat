-- @testpoint: 使用or逻辑运算符查询
drop table  if exists t_student;
create table  t_student(stu_name char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into  t_student(stu_age,stu_name) values(25,'wangwuxiao'),(28,'lizi'),(40,'zhaosi');
select * from t_student where stu_age >25 or stu_age >28;
--清理环境
drop table if exists t_student cascade;