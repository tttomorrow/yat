-- @testpoint: 创建时设置CYCLE 修改cache 合理报错

--创建序列
drop sequence if exists test_seq_011;
CREATE sequence test_seq_011 minvalue 1 maxvalue 10  cycle;
drop table if exists table_seq_011 cascade;
create table table_seq_011(id int);
--查询cache值
select last_value,cache_value from test_seq_011;

--修改cache*步长 小于最小值 期望：修改失败 合理报错
alter sequence test_seq_011 cache -10;
--查询cache值
select last_value,cache_value from test_seq_011;
select nextval('test_seq_011');
insert into table_seq_011 values(nextval('test_seq_011'));
alter sequence test_seq_011 maxvalue 15;
select last_value,cache_value,max_value from test_seq_011;
select nextval('test_seq_011');

--修改cache*步长 大于最大值 期望：修改成功
alter sequence test_seq_011 cache 15;
--查询cache值
select last_value,cache_value from test_seq_011;
select nextval('test_seq_011');
insert into table_seq_011 values(nextval('test_seq_011'));
alter sequence test_seq_011 maxvalue 15;
select last_value,cache_value,max_value from test_seq_011;
select nextval('test_seq_011');

--修改cache*步长 大于最小值小于最大值 期望：修改成功
alter sequence test_seq_011 cache 15;
--查询cache值
select last_value,cache_value from test_seq_011;
select nextval('test_seq_011');
insert into table_seq_011 values(nextval('test_seq_011'));
alter sequence test_seq_011 maxvalue 15;
select last_value,cache_value,max_value from test_seq_011;
select nextval('test_seq_011');

--清理环境
drop table if exists table_seq_011 cascade;
drop sequence if exists test_seq_011;