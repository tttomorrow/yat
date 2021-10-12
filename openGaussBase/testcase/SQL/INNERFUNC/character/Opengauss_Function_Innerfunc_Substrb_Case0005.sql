-- @testpoint: 起始位参数起始位置为0或者负数小数
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('jfkfkd');
SELECT substrb(string1,0,6) from type_char;
SELECT substrb(string1,-2,3) from type_char;
SELECT substrb(string1,2.1,3) from type_char;
DROP TABLE IF EXISTS type_char;