-- @testpoint: 类型转换函数to_char(int, text)，入参超边界值时合理报错

-- 左边界值取不到
select to_char(-32768::smallint, '9999999');

-- 边界值上下
select to_char(-32769::smallint, '9999999');
select to_char(32768::smallint, '9999999');



-- 指定长度不足
select to_char(32767::smallint, '999');
