-- @testpoint: 类型转换函数rawtohex(string)，将一个二进制构成的字符串转换为十六进制的字符串，入参为有效值

-- 数据呈现是字符串 字符的asiic编码是10进制 是asiic编码的集合被转换成16进制
-- A:65:41
select rawtohex('A');
select rawtohex('AaBb');

-- 1:49:31
select rawtohex('1');
select rawtohex('3');

select rawtohex('1234567');

-- #:35:23
select rawtohex('#&!@');

--汉字
select rawtohex('汉字');