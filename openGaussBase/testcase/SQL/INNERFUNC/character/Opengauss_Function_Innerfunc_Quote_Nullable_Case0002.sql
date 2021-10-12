-- @testpoint: 参数为浮点型
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 text);
insert into type_char values (quote_nullable(5.5));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;