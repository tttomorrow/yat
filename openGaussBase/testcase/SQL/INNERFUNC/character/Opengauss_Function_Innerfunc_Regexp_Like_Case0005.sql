-- @testpoint: 参数c定义时大小写不匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('abc');
SELECT regexp_like(string1,'[A-Z]','c') from type_char;
DROP TABLE IF EXISTS type_char;