-- @testpoint: 参数为时间
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 text);
insert into type_char values (quote_nullable(2017-1-9));
SELECT * from type_char;
DROP TABLE IF EXISTS type_char;