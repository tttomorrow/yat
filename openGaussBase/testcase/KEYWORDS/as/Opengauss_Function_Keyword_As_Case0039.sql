-- @testpoint: 列名为as，并且定义as和default
drop table if exists  test_as_005;
create table  test_as_005 ("as" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
drop table if exists  test_as_005;