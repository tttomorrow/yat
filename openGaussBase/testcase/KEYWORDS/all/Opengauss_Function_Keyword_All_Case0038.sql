-- @testpoint: 关键字all带双引号作为普通表的列名在insert语句的使用
drop table if exists  test_and_002;
create table test_and_002 ("all" int);
insert into test_and_002 ("all")values(20);
drop table if exists  test_and_002;