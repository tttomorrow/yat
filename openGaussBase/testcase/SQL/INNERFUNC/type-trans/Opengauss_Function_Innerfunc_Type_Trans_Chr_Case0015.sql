-- @testpoint: to_char (numeric/smallint/integer/bigint/double precision/real[, fmt])将一个整型或者浮点类型的值转换为指定格式的字符串，入参超出边界值时合理报错

-- p<1、p>1000、p为浮点数
select to_char(-123.456::numeric(-1,3),'999D999s');
select to_char(-123.456::numeric(1001,3),'999D999s');
select to_char(-123.456::numeric(3.7,3),'999D999s');

-- s<0 、s为浮点数
select to_char(-123.456::numeric(6,-3),'999D999s');
select to_char(-123.456::numeric(6,2.9),'999D999s');

--整数位> 、< p-s 抛出异常
select to_char(-1239.456::numeric(6,3),'9999D999s');
select to_char(-1239.456::numeric(8,3),'9999D999s');

-- 指定长度不足
select to_char(32767::SMALLINT, '999');
select to_char(-2147483647::INT4, '999999');
select to_char(9223372036854775807::BIGINT, '99999999');

-- 指定格式错误
select to_char(-1239.456::numeric(7,3),'*&……%￥','999');
select to_char(-1239.456::numeric(7,3),''汉字'');

-- 多参、少参
select to_char(485, '9 9 9','jij');
select to_char();
select to_char(156*&%$%^x);
