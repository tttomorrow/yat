-- @testpoint: 中文
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('我是');
SELECT quote_literal(string1) from type_char;
DROP TABLE IF EXISTS type_char;