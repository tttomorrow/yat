-- @testpoint: 字符串为空
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('');
SELECT substrb(string1,10,5) from type_char;
DROP TABLE IF EXISTS type_char;