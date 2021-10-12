-- @testpoint: 模式匹配操作符SIMILAR TO,使用元字符+，重复项为多个字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('abcabcbababcd');
SELECT  * from type_char  where string1 SIMILAR TO '(abc)+bababcd';
DROP TABLE IF EXISTS type_char;