-- @testpoint: 参数2给空值
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 RAW,string2 RAW);
insert into type_char(string1) values ('abcdeF');
SELECT rawcat(string1,string2) from type_char;
DROP TABLE IF EXISTS type_char;