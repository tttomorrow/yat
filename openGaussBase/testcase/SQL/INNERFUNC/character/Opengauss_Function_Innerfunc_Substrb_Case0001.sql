-- @testpoint: 起始位大于字符串长度
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('trimxxxx');
SELECT substrb(string1,10,5) from type_char;
DROP TABLE IF EXISTS type_char;