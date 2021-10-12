-- @testpoint: 模式匹配操作符LIKE,匹配串内序列，未以百分号开头和结尾
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('abc');
SELECT * from type_char  where string1 LIKE 'a';
DROP TABLE IF EXISTS type_char;