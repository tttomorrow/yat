-- @testpoint: 没有参数，合理报错
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 RAW,string2 RAW);
SELECT rawcat() from type_char;
DROP TABLE IF EXISTS type_char;