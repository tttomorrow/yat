-- @testpoint: 打印一份详细的清理工作报告
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10),score int,address char(10));
vacuum (verbose, analyze) t_student;
drop table if exists t_student;