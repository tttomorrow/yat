-- @testpoint: 全是十六进制数，包含大小写及数字
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 RAW,string2 RAW);
SELECT rawcat(string1,string2) from type_char;
DROP TABLE IF EXISTS type_char;