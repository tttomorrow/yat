-- @testpoint: rawtohex函数异常校验，合理报错
SELECT rawtohex('a','b');
SELECT rawtohex();
SELECT rawtohex('');
SELECT rawtohex(null);