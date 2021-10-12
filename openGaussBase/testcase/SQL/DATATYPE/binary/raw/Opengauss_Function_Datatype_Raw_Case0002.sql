-- @testpoint: 插入0值
-- @modify at: 2020-11-04

--创建表
drop table if exists test_raw02;
create table test_raw02 (name raw);

--插入数据
insert into test_raw02 values (HEXTORAW('0'));

--插入成功，插入数据
select * from test_raw02;

--清理环境
drop table test_raw02;