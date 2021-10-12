-- @testpoint: 超出内存长度
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 text);
insert into type_char values ('abcdel');
SELECT repeat(string1,100000) from type_char;
DROP TABLE IF EXISTS type_char;