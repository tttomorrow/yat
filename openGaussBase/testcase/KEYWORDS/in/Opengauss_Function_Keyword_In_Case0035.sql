-- @testpoint: 查询使用in
drop table if exists test_dsc_01;
create table  test_dsc_01(stu_name char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into  test_dsc_01(stu_age,stu_name) values(25,'wangwuxiao'),(28,'lizi'),(40,'zhaosi');
select * from test_dsc_01  where stu_age in(25,28);
--清理环境
drop table if exists test_dsc_01 cascade;


