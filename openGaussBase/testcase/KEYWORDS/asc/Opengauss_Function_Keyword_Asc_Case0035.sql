-- @testpoint: 定义和使用列时不使用asc,排序时不加asc关键字
drop table if exists test_asc_01;
create table  test_asc_01(stu_name char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into  test_asc_01(stu_age,stu_name) values(25,'wangwuxiao'),(28,'lizi'),(40,'zhaosi');
select* from test_asc_01 order by stu_name;
drop table if exists test_asc_01;