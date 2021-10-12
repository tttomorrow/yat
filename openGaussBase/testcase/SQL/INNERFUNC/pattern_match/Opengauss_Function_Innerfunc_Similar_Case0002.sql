-- @testpoint: 模式匹配操作符SIMILAR TO,匹配串内的序列，模式未以百分号开头和结尾
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(10));
insert into type_char values ('abcd');
SELECT  * from type_char  where string1 SIMILAR TO 'abc';
DROP TABLE IF EXISTS type_char;