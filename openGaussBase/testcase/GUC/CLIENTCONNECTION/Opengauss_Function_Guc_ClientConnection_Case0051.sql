-- @testpoint: 使用set方法设置参数check_function_bodies为off，默认为on下，创建函数无参返回值有参函数，合理报错
--查看默认
show check_function_bodies;
--创建函数,报错
CREATE or replace FUNCTION bad051_bak() RETURNS void
LANGUAGE sql
AS 'SELECT $1';
/
--设置
set check_function_bodies to off;
--查看
show check_function_bodies;
--创建函数,成功
CREATE or replace FUNCTION bad051() RETURNS void
LANGUAGE sql
AS 'SELECT $1';
/
--恢复默认
set check_function_bodies to on;
show check_function_bodies;
drop FUNCTION bad051;