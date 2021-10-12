-- @testpoint: 创建时设置minvalue/maxvalue和步长 修改cache 合理报错

--创建序列
drop sequence if exists test_seq_010;
CREATE sequence test_seq_010 increment 2 minvalue 1 maxvalue 11;
drop table if exists table_seq_010 cascade;
create table table_seq_010(id int);
--查询cache值
select last_value,cache_value from test_seq_010;

--修改cache*步长 小于最小值 期望：修改成功 清空cache后调用时合理报错
alter sequence test_seq_010 cache -5;
--查询cache值
select last_value,cache_value from test_seq_010;
select nextval('test_seq_010');
insert into table_seq_010 values(nextval('test_seq_010'));
alter sequence test_seq_010 maxvalue 51;
select last_value,cache_value,max_value from test_seq_010;

--修改cache*步长 大于最大值 期望：修改成功 清空cache后调用时合理报错
alter sequence test_seq_010 cache 7;
--查询cache值
select last_value,cache_value from test_seq_010;
select nextval('test_seq_010');
insert into table_seq_010 values(nextval('test_seq_010'));
alter sequence test_seq_010 maxvalue 13;
select last_value,cache_value,max_value from test_seq_010;
select nextval('test_seq_010');

--修改cache*步长 小于于最大值大于最小值 期望：修改成功
alter sequence test_seq_010 cache 10;
--查询cache值
select last_value,cache_value from test_seq_010;
alter sequence test_seq_010 maxvalue 21;
select last_value,cache_value,max_value from test_seq_010;
select nextval('test_seq_010');

--清理环境
drop table if exists table_seq_010 cascade;
drop sequence if exists test_seq_010;
