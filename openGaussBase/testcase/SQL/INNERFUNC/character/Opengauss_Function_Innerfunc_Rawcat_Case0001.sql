-- @testpoint: 参数2不为十六进制，合理报错
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 RAW,string2 char(100));
insert into type_char values ('DEADBEEF','khj');
SELECT rawcat(string1,string2) from type_char;
DROP TABLE IF EXISTS type_char;