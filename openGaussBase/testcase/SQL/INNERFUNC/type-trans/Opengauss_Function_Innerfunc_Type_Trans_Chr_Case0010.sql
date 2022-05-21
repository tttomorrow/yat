-- @testpoint: 类型转换函数to_char(int, text)整数类型的值转换为指定格式的字符串，入参为有效值

select to_char(125, '999');

--tinyint、smallint、integer、bigint
select to_char(125::tinyint, '999');
select to_char(0::tinyint, '999');

select to_char(-32767::smallint, '9999999s');
select to_char(0::smallint, '999');
select to_char(32767::smallint, '9999999');

select to_char(-2147483647::int4, '9999999999999999');
select to_char(0::int4, '999');
select to_char(2147483647::integer, '9999999999999999');

select to_char(-9223372036854775807::bigint, '99999999999999999999999');
select to_char(0::bigint, '999');
select to_char(9223372036854775807::bigint, '99999999999999999999999');

-- 0
select to_char(32767::smallint, '000');
select to_char(32767::smallint, '000009');
select to_char(32767::smallint, '00000');
