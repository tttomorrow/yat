-- @testpoint: 更新时，使用as列
drop table if exists test_as_007;
create table  test_as_007 ("as" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into test_as_007("as") values('zhangsan');
update test_as_007 set "as"='lisi';
drop table if exists test_as_007;