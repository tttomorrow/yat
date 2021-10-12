-- @testpoint: 带模式和不带模式指定转换函数，带模式合理报错

--创建模式
drop schema if exists testCast cascade;
create schema testCast;

--testpoint：不带模式指定转换函数：success
explain performance select cast('2020-09-29' as date);

--testpoint：带模式指定转换函数：合理报错
explain performance select testCast.cast('2020-09-29' as date);

--清理环境
drop schema if exists testCast cascade;