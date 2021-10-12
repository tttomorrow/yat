-- @testpoint: 创建基于多个字段的表达式索引

--1.创建表插入数据
create table t_tb(num1 int, num2 int);
insert into t_tb values(generate_series(1,1000), generate_series(1000,2000));
--2.创建函数
create function func_multi(num1 int, num2 int) return int
IMMUTABLE
as
begin
return num1*num2;
end;
/
--3.创建索引
drop index if exists idx;
create index idx on t_tb(func_multi(num1, num2));
--4.使用索引
SET ENABLE_SEQSCAN=off;
explain select count(num1) from t_tb where func_multi(num1, num2)>10000;
select count(num1) from t_tb where func_multi(num1, num2)>10000;

--tearDown
drop table if exists t_tb cascade;
drop function func_multi;