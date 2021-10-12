-- @testpoint: 正常字符颠倒
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 text);
insert into type_char values ('abcdel');
SELECT reverse(string1) from type_char;
DROP TABLE IF EXISTS type_char;