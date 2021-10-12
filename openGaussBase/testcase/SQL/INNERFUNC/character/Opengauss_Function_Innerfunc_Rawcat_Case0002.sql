-- @testpoint: 多参，期待合理报错
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 RAW,string2 RAW,string3 RAW);
insert into type_char values ('DEADBEEF','ab','cd');
SELECT rawcat(string1,string2,string3) from type_char;
DROP TABLE IF EXISTS type_char;