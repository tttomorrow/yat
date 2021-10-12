-- @testpoint: 模式匹配操作符SIMILAR TO,使用[...]声明一个数字字符类
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 int);
insert into type_char values (123);
SELECT  * from type_char  where string1 SIMILAR TO '[0-9]23';
DROP TABLE IF EXISTS type_char;