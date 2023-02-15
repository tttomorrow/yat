-- @testpoint: cast用例,部分用例合理报错
-- cast函数输入参数,timestamp转换为unsigned
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('2022-11-10 183:03:20'::timestamp as unsigned);
select cast('2022-11-10 83:03:20'::timestamp as unsigned);
