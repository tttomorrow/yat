-- @testpoint: 修改已存在列的数据类型
drop table  if exists t_student;
create table  t_student(stu_name char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into  t_student(stu_age,stu_name) values(25,'wangwuxiao'),(28,'lizi'),(40,'zhaosi');
alter table t_student modify (stu_name text);
--清理环境
drop table  if exists t_student;
