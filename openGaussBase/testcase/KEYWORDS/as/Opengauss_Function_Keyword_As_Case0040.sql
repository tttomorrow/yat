-- @testpoint: 插入时，使用as列
drop table if exists test_as_006;
create table test_as_006 ("as" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into test_as_006("as") values('zhangsan');
drop table if exists test_as_006;