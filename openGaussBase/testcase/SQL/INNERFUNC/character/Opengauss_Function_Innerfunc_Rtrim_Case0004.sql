-- @testpoint: 汉字搜索
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('我是一个');
SELECT rtrim(string1,'一个') from type_char;
DROP TABLE IF EXISTS type_char;