-- @testpoint: 同义词连接对象不存在，创建成功，查询，合理报错
-- @modify at: 2020-11-25
--创建同义词，表不存在
drop table if exists test_SYN_048;
drop synonym if exists SYN_048;
create synonym SYN_048 for test_SYN_048;
--查询，合理报错
select * FROM SYN_048;
select * from test_SYN_048;
--删除同义词
drop synonym if exists SYN_048;