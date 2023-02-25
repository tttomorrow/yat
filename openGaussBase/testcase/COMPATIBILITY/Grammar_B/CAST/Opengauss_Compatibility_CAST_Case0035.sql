-- @testpoint: cast用例,部分用例合理报错
-- cast函数输入参数,money转换为unsigned
select cast('$2'::money as unsigned);
select cast(cast('$244566'::money as unsigned) as money);
select cast(cast('$-190'::money as unsigned) as money);
