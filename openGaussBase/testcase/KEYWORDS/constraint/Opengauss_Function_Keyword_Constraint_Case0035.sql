--  @testpoint:创建表时指定字段的约束
drop table if exists  t_student;
create table t_student (stu_name char(20) not null,stu_age int,sex char(10) not null,score int,address char(10));
drop table t_student;