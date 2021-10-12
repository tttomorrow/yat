-- @testpoint: 参数i定义时大小写匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('ABC');
SELECT regexp_like(string1,'[A-Z]','i') from type_char;
DROP TABLE IF EXISTS type_char;