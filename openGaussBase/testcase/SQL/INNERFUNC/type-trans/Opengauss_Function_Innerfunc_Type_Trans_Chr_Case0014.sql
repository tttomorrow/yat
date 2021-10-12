-- @testpoint: 类型转换函数to_char (numeric/smallint/integer/bigint/double precision/real[, fmt])将一个整型或者浮点类型的值转换为指定格式的字符串，入参为有效值

-- 整型
select to_char(12, '9990999.9');
select to_char(12, 'FM9990999.9');
select to_char(485, '999');
select to_char(-485, '999');
select to_char(485, '9 9 9');
select to_char(-485, '999S');
select to_char(-485, '999MI');
select to_char(485, '999MI');
select to_char(485, 'FM999MI');
select to_char(485, 'PL999');
select to_char(485, 'SG999');
select to_char(-485, 'SG999');
select to_char(-485, '9SG99');
select to_char(-485, '999PR');
select to_char(485, 'L999');
select to_char(485, 'RN');
select to_char(485, 'FMRN');
select to_char(482, '999th');
select to_char(485, '"Good number:"999');
select to_char(12, '99V999');
select to_char(123,'XXX');

-- 浮点类型
select to_char(-0.1, '99.99');
select to_char(-0.1, 'FM9.99');
select to_char(0.1, '0.9');
select to_char(1485, '9,999');
select to_char(1485, '9G999');
select to_char(148.5, '999.999');
select to_char(148.5, 'FM999.999');
select to_char(148.5, 'FM999.990');
select to_char(148.5, '999D999');
select to_char(3148.5, '9G999D999');
select to_char(5.2, 'FMRN');
select to_char(485.8, '"Pre:"999" Post:" .999');
select to_char(12.4, '99V999');
select to_char(12.45, '99V9');
select to_char(0.0004859, '9.99EEEE');


