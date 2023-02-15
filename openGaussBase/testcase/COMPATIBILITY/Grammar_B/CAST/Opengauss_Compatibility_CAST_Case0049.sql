-- @testpoint: cast用例,部分用例合理报错
-- 转换后的值参与运算或函数中
select cast('2022-11-10 :03:20'::timestamp as unsigned);
select cast('2022-11 18:03:20'::timestamp as unsigned);
select cast('2022-11-10 18:03'::timestamp as unsigned);
select cast('$2'-'$5'::money as unsigned);
select cast('$2'-'$2'::money as unsigned);
