-- @testpoint: 定义as列带双引号，使用时不带，合理报错
drop table if exists test_as_012;
create table  test_as_012("as" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into  test_as_012(stu_age,as) values(25,'wangwuxiao');
drop table if exists test_as_012;