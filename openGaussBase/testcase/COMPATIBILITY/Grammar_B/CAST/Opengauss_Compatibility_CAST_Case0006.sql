-- @testpoint: cast用例,部分用例合理报错,部分用例合理报错
-- cast函数输入参数，as前后有多个type及expr
select cast('$2'::money as unsigned money);
select cast(cast('$2'::money as unsigned) as money,unsigned);
select cast('2022-11-10 18:03:20'::timestamp,'2022-11-10 18:03:20'::timestamp as unsigned,money);
select cast(current_timestamp::timestamp current_timestamp::timestamp as unsigned money);
select cast(cast('2022-11-10 18:03:20'::timestamp as unsigned) as timestamp timestamp timestamp);
