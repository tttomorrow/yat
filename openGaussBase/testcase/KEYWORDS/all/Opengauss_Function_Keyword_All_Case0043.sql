-- @testpoint: 列名为带引号的all，并且定义all和default
drop table if exists student_tb1;
create table student_tb1 ("all" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
drop table if exists student_tb1;