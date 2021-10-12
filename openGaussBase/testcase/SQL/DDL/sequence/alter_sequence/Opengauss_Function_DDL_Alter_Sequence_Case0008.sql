-- @testpoint: 创建时设置cache 插值和插入值后执行alter sequence cache 修改cache为正确和错误值等 合理报错

--创建序列
drop sequence if exists test_seq_008;
CREATE sequence test_seq_008 cache 10;
drop table if exists table_seq_008 cascade;
create table table_seq_008(id int);
--查询cache值
select last_value,cache_value from test_seq_008;

--未调用时修改cache值
alter sequence test_seq_008 cache 20;
--查询cache值
select last_value,cache_value from test_seq_008;
alter sequence test_seq_008 maxvalue 50;
select last_value,cache_value from test_seq_008;
alter sequence test_seq_008 cache 5;
select last_value,cache_value from test_seq_008;

--调用后修改cache
select nextval('test_seq_008');
insert into table_seq_008 values(nextval('test_seq_008'));
alter sequence test_seq_008 cache 20;
--查询cache值
select last_value,cache_value from test_seq_008;
alter sequence test_seq_008 maxvalue 50;
select last_value,cache_value from test_seq_008;
alter sequence test_seq_008 cache 5;
select last_value,cache_value from test_seq_008;

--alter为-1，0，字母 浮点数空格等无效值 合理报错
alter sequence test_seq_008 cache -1.1;
alter sequence test_seq_008 cache 0;
alter sequence test_seq_008 cache 'aa';
alter sequence test_seq_008 cache '';
alter sequence test_seq_008 cache '!==()*';

--查询cache值
select last_value,cache_value from test_seq_008;

--清理环境
drop table if exists table_seq_008 cascade;
drop sequence if exists test_seq_008;