-- @testpoint: 插入字符串形式二进制
-- @modify at: 2020-11-04

--创建表
drop table if exists test_blob04;
create table test_blob04 (name blob);

--插入数据
insert into test_blob04 values ('1010101');

--插入成功，查看数据
select * from test_blob04;

--清理环境
drop table test_blob04;