-- @testpoint: 类型转换函数to_char将浮点类型的值转换为指定格式的字符串，入参为空值、特殊字符、多参、少参、其它进制、其它类型时合理报错

SELECT to_char(0X89, '999D99');

SELECT to_char('OPENGUASS', '999D99');

SELECT to_char(, '999D99');

SELECT to_char(1122.345 ' ');

SELECT to_char(125.8::real, '999D99','9999D99');