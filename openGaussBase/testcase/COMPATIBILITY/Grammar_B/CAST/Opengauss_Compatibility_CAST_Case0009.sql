-- @testpoint: cast用例
-- 设置时区
set time zone 'uct';
-- cast函数输入参数，as前为expr，后为type
select cast('$2'::money as unsigned);
select cast(cast('$2'::money as unsigned) as money);
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
set time zone 'uct';
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
