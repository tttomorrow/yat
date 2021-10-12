-- @testpoint: 模式匹配操作符SIMILAR TO,使用[...]声明一个字符类
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('abc');
SELECT  * from type_char  where string1 SIMILAR TO '[ab]bc';
DROP TABLE IF EXISTS type_char;