-- @testpoint: 入参是数字
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 int);
insert into type_char values (1234565);
SELECT substrb(string1,1,3) from type_char;
DROP TABLE IF EXISTS type_char;