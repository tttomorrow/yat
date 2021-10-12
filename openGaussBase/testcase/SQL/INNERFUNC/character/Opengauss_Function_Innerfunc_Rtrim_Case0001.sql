-- @testpoint: 最后一位不是搜索字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('trimxxxx');
SELECT rtrim(string1,'y') from type_char;
DROP TABLE IF EXISTS type_char;