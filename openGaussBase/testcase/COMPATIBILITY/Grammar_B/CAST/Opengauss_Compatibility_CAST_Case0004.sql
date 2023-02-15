-- @testpoint: cast用例,部分用例合理报错
-- cast函数输入参数，as前后边均是type
-- 设置时区
set time zone 'uct';
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
set time zone 'uct';
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('$2'::money as unsigned);
select cast(cast('$2'::money as unsigned) as money);
