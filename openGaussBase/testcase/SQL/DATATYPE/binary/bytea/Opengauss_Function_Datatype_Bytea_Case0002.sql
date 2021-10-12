-- @testpoint: 插入负数
-- @modify at: 2020-11-04

--创建表
drop table if exists test_bytea02;
create table test_bytea02 (name bytea);

--插入数据
insert into test_bytea02 values ('-1');

--插入成功，查看数据
select * from test_bytea02;

--清理环境
drop table test_bytea02;