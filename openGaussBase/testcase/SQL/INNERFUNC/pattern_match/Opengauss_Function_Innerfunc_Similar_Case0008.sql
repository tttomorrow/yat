-- @testpoint: 模式匹配操作符SIMILAR TO,使用元字符*，重复前面的项零次或更多次去匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(10));
insert into type_char values ('bcd');
SELECT  * from type_char  where string1 SIMILAR TO 'c*bcd';
DROP TABLE IF EXISTS type_char;