-- @testpoint: cast用例,部分用例合理报错
--设置时区
set time zone 'uct';
-- 转换后的值参与运算或函数中
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('$2'-'$5'::money as unsigned);
select cast('$2'-'$2'::money as unsigned);
select cast('$6'-'$2'::money as unsigned);
select cast('2022-11-10 18:03:20'-'2022-11-10 18:03:01'::timestamp as unsigned);
