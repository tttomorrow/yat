-- @testpoint: rawtohex函数入参为特殊字符
SELECT rawtohex('~');
SELECT rawtohex('@');
SELECT rawtohex('#');
SELECT rawtohex('$');
SELECT rawtohex('%');
SELECT rawtohex('^');
SELECT rawtohex('&');
SELECT rawtohex('*');
SELECT rawtohex('(');
SELECT rawtohex(')');
SELECT rawtohex(',');
SELECT rawtohex('+');