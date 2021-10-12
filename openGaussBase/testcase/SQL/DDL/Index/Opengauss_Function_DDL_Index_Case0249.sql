-- @testpoint: 创建表达式索引，使用括号或不使用，合理报错

--1.创建表
create table t_tb(i int);
--2.创建表达式索引，不带括号
create index idx on t_tb(i+2);
--3.创建表达式索引，带括号
create index idx on t_tb((i+2));
--4.插入数据
insert into t_tb values(generate_series(1,20000));
--5.使用索引
SET ENABLE_SEQSCAN=off;
explain select count(*) from t_tb where i+2>1000;
select count(*) from t_tb where i+2>1000;
--6.创建函数
create function func_double(num int) return int
IMMUTABLE
as
begin
return num*2;
end;
/
--7.创建索引，不使用括号
drop index if exists idx;
create index idx on t_tb(func_double(i));
--8.使用索引
SET ENABLE_SEQSCAN=off;
explain select count(*) from t_tb where func_double(i)>1000;
select count(*) from t_tb where func_double(i)>1000;
--9.创建索引，使用括号
drop index if exists idx;
create index idx on t_tb(func_double(i));
--10.使用索引
SET ENABLE_SEQSCAN=off;
explain select count(*) from t_tb where func_double(i)>1000;
select count(*) from t_tb where func_double(i)>1000;

--tearDown
drop table if exists t_tb cascade;
drop function func_double;