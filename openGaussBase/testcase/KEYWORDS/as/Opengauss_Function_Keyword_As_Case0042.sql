-- @testpoint: 删除时，使用as列
drop table if exists test_as_008;
create table test_as_008 ("as" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into test_as_008("as") values('zhangsan');
delete from  test_as_008 where "as"='zhangsan';
drop table if exists test_as_008;