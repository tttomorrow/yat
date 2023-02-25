-- @testpoint: cast用例,部分用例合理报错,部分用例合理报错
-- cast函数输入参数，as前是type后边是表达式
select cast(timestamp as now());
select cast(timestamp as 1);
select cast('2022-11-10 18:03:20'::timestamp as true);
select cast('$2'::money as select current_timestamp);

