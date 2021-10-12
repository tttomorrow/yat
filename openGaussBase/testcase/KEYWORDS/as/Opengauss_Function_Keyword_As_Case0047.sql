-- @testpoint: 定义和使用as列带双引号
drop table if exists  test_as_013;
create table  test_as_013("as" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into  test_as_013(stu_age,"as") values(25,'wangwuxiao');
select * from test_as_013;
drop table if exists  test_as_013;