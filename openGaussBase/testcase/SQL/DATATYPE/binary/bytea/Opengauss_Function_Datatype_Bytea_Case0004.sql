-- @testpoint: 插入字符串形式二进制数
-- @modify at: 2020-11-04

--创建表
drop table if exists test_bytea04;
create table test_bytea04 (name bytea);

--插入数据
insert into test_bytea04 values ('1010101');

--插入成功，查看数据
select * from test_bytea04;

--清理环境
drop table test_bytea04;
