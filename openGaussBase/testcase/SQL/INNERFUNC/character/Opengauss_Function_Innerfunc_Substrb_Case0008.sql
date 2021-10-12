-- @testpoint: 只有起始位参数起始位置为0或者负数小数
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('abc');
SELECT substrb(string1,0) from type_char;
SELECT substrb(string1,-2) from type_char;
SELECT substrb(string1,1.1) from type_char;
DROP TABLE IF EXISTS type_char;