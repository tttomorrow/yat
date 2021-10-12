-- @testpoint: 类型转换函数，rawtohex(string)将一个二进制构成的字符串转换为十六进制的字符串，入参为无效值时合理报错

-- 多参，少参、空值
SELECT rawtohex();
SELECT rawtohex('A','999');
SELECT rawtohex(汉字);
SELECT rawtohex(0x12L);