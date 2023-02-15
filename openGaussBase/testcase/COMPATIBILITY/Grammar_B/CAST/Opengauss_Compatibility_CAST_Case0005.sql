-- @testpoint: cast用例,部分用例合理报错,部分用例合理报错
set time zone 'uct';
-- cast函数输入参数，as前后边是expr
select cast(0 as 1);
select cast(cast(0 as money) as money);
select cast(cast(true as money) as money);
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('2022-11-10 18:03:20'::timestamp as true);
select cast('2022-11-10 18:03:20'::timestamp as 0);
select cast(-1 as timestamp);
select cast(-111 as timestamp);
select cast(221 as timestamp);
