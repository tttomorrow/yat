-- @testpoint: 求一列的平均值
drop table if exists test_avg_01;
create table  test_avg_01(stu_name char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into  test_avg_01(stu_age,stu_name) values(25,'wangwuxiao'),(28,'lizi'),(40,'zhaosi');
select avg(stu_age) from test_avg_01;
drop table if exists test_avg_01;
