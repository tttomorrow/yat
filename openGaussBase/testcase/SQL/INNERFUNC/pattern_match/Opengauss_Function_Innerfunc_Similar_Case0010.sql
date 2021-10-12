-- @testpoint: 模式匹配操作符SIMILAR TO,使用元字符*，重复项为一个字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(10));
insert into type_char values ('abcd');
SELECT  * from type_char  where string1 SIMILAR TO 'a*bcd';
DROP TABLE IF EXISTS type_char;