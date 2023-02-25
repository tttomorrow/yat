-- @testpoint: cast用例,部分用例合理报错
-- cast函数输入参数，as前为其他类型的expr
select cast(select current_timestamp as unsigned);
select cast(unsigned as select current_timestamp);
select cast(unsigned as select now());
select cast(select now() as unsigned);
