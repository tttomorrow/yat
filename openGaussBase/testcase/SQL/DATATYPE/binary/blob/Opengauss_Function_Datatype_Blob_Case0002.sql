-- @testpoint: 插入负数,合理报错
-- @modify at: 2020-11-04

--创建表
drop table if exists test_blob02;
create table test_blob02 (name blob);

--插入负数，合理报错
insert into test_blob02 values ('-1');

--插入失败，查看数据
select * from test_blob02;

--清理环境
drop table test_blob02;
