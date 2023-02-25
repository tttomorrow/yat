-- @testpoint: cast用例
-- 设置时区
set time zone 'uct';
-- cast函数输入参数,timestamp转换为unsigned
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
-- 设置时区
set time zone 'uct';
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('2022-11-10'::timestamp as unsigned);
select cast('18:03:20'::timestamp as unsigned);
