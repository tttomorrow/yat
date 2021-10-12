--  @testpoint:列名出现关键字and；and大小写混合,不带双引号and应该报错
drop table if exists student_tb1;
create table student_tb1 (And char(20),stu_age int,sex char(10),score int,address char(10));