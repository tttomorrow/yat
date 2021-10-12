-- @testpoint: 小数和1
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 text);
insert into type_char values ('abcdeF kk');
SELECT repeat(string1,1.1) from type_char;
SELECT repeat(string1,1) from type_char;
DROP TABLE IF EXISTS type_char;