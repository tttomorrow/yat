-- @testpoint: 起始位和取字符长度都缺省
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('abcd');
SELECT substrb(string1) from type_char;
DROP TABLE IF EXISTS type_char;