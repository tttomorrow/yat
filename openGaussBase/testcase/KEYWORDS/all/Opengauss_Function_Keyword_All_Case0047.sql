-- @testpoint: 定义表的别名为all
drop table if exists t_student;
create table t_student (stu_name char(20),stu_age int,sex char(10),score int,address char(10));
drop table if exists "all";
alter table  t_student rename to "all";
select * from "all";
drop table if exists t_student;
drop table if exists "all";