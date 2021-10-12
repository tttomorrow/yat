-- @testpoint: 创建时设置maxvalue 和 minvalue 修改cache 合理报错

--创建序列
drop sequence if exists test_seq_009;
CREATE sequence test_seq_009 minvalue 1 maxvalue 10;
drop table if exists table_seq_009 cascade;
create table table_seq_009(id int);
--查询cache值
select last_value,cache_value from test_seq_009;

--修改cache大于最小值小于最大值 期望：修改成功
alter sequence test_seq_009 cache 5;
--查询cache值
select last_value,cache_value from test_seq_009;
select nextval('test_seq_009');
insert into table_seq_009 values(nextval('test_seq_009'));
select last_value,cache_value from test_seq_009;
select nextval('test_seq_009');

--修改cache大于最大值 期望：修改成功 清空cache后调用时合理报错
alter sequence test_seq_009 cache -10;
--查询cache值
select last_value,cache_value from test_seq_009;
alter sequence test_seq_009 maxvalue 50;
select nextval('test_seq_009');
insert into table_seq_009 values(nextval('test_seq_009'));
select last_value,cache_value from test_seq_009;
select nextval('test_seq_009');

--修改cache小于最小值 期望：修改成功 清空cache后调用时合理报错
alter sequence test_seq_009 cache -20;
--查询cache值
select last_value,cache_value from test_seq_009;
alter sequence test_seq_009 maxvalue 50;
select nextval('test_seq_009');
insert into table_seq_009 values(nextval('test_seq_009'));
select last_value,cache_value from test_seq_009;
select nextval('test_seq_009');

--清理环境
drop table if exists table_seq_009 cascade;
drop sequence if exists test_seq_009;