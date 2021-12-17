-- @testpoint: 类型转换函数to_char(int, text)，入参超边界值时合理报错

-- 左边界值取不到
select to_char(-32768::smallint, '9999999');
select to_char(-2147483648::int4, '9999999999999999');
select to_char(-9223372036854775808::bigint, '99999999999999999999999');

-- 边界值上下
select to_char(-32769::smallint, '9999999');
select to_char(32768::smallint, '9999999');

select to_char(-2147483649::int4, '9999999999999999');
select to_char(2147483648::int4, '9999999999999999');

select to_char(-9223372036854775809::bigint, '99999999999999999999999');
select to_char(9223372036854775808::bigint, '99999999999999999999999');

-- 指定长度不足
select to_char(32767::smallint, '999');
select to_char(-2147483647::int4, '999999');
select to_char(9223372036854775807::bigint, '99999999');