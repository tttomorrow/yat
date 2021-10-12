-- @testpoint: 定义and列带双引号，使用时不带，合理报错
drop table if exists t_student;
create table  t_student ("and" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into t_student(stu_age,and) values(25,'wangwuxiao');
drop table if exists t_student;