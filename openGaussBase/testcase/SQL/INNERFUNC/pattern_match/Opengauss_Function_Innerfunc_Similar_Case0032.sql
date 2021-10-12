-- @testpoint: 模式匹配操作符SIMILAR TO,模式中包含中文字符
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('我bababcd');
SELECT  * from type_char  where string1 SIMILAR TO '我{1}bababcd';
DROP TABLE IF EXISTS type_char;