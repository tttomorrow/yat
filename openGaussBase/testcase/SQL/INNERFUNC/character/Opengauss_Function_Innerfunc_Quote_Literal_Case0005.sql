-- @testpoint: 不是一个字符类型
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 int);
insert into type_char values (111);
SELECT quote_literal(string1) from type_char;
DROP TABLE IF EXISTS type_char;