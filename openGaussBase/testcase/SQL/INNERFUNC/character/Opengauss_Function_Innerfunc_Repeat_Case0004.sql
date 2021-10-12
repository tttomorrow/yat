-- @testpoint: text类型
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 text);
insert into type_char values ('abcdeF kk');
SELECT repeat(string1,2) from type_char;
DROP TABLE IF EXISTS type_char;