-- @testpoint: 提取字符为0或者负数小数
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('jfkfkd');
SELECT substrb(string1,1,0) from type_char;
SELECT substrb(string1,1,-1) from type_char;
SELECT substrb(string1,1,2.5) from type_char;
DROP TABLE IF EXISTS type_char;