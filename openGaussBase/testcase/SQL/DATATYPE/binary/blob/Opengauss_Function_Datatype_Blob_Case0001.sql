-- @testpoint: 插入正常值
-- @modify at: 2020-11-04

--创建表
drop table if exists test_blob01;
create table test_blob01 (name blob);

--插入blob类型的值
insert into test_blob01 values ('01010101');

--插入成功，查询数据
select * from test_blob01;

--清理环境
drop table test_blob01;

