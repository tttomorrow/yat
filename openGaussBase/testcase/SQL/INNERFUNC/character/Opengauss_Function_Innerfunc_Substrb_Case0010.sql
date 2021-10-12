-- @testpoint: 只有起始位参数起始位置大于字符长度
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('');
SELECT substrb(string1,1) from type_char;
DROP TABLE IF EXISTS type_char;