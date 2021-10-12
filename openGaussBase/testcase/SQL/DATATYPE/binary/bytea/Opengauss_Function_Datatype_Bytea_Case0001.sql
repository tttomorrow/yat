-- @testpoint: 插入正常值
-- @modify at: 2020-11-04

--创建表
drop table if exists test_bytea01;
create table test_bytea01 (name bytea);

--插入数据
insert into test_bytea01 values ('01010101');

--插入成功，查看数据
select * from test_bytea01;

--清理环境
drop table test_bytea01;