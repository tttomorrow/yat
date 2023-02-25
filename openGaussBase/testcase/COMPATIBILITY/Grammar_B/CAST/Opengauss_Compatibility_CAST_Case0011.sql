-- @testpoint: cast用例
-- cast函数输入参数,money转换为unsigned
select cast('$2'::money as unsigned);
select cast(cast('$2'::money as unsigned) as money);
select cast(cast('$90'::money as unsigned) as money);
select cast('$200'::money as unsigned);
