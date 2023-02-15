-- @testpoint: cast用例,部分用例合理报错,部分用例合理报错
-- cast函数输入参数，as后为不存在的type
select cast('$2'::money as unsigne);
select cast(cast('$2'::money as unsigned) as $);
select cast('2022-11-10 18:03:20'::timestamp as unsign);
select cast(current_timestamp::timestamp as unsigned1);
select cast(cast('2022-11-10 18:03:20'::timestamp as unsigned) as time stamp);
select cast(cast('2022-11-10 18:03:20'::timestamp as unsigned) as timestamp1);
