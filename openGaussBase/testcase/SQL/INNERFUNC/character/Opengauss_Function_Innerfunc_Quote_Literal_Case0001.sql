-- @testpoint: 参数为null
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('');
SELECT quote_literal(string1) from type_char;
DROP TABLE IF EXISTS type_char;