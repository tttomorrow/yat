-- @testpoint: 插入正常值
-- @modify at: 2020-11-04

--创建表
drop table if exists test_raw01;
create table test_raw01 (name raw);

--插入数据
insert into test_raw01 values (HEXTORAW('DEADBEEF'));

--插入成功，查看数据
select * from test_raw01;

--清理环境
drop table test_raw01;