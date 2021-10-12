-- @testpoint: rawtohex函数入参为比较表达式，合理报错
SELECT rawtohex(2<3);
SELECT rawtohex(8>7);
SELECT rawtohex(1=1);
