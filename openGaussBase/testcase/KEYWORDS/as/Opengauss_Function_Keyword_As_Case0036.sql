-- @testpoint: 定义和使用as列带双引号
drop table if exists  test_as_002;
create table test_as_002 ("as" int);
insert into test_as_002 ("as")values(20);
drop table if exists  test_as_002;