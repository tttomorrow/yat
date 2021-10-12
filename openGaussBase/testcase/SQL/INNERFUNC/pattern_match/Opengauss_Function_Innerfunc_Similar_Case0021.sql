-- @testpoint: 模式匹配操作符SIMILAR TO,使用元字符{m,} ,重复前面的项0次去匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('bababcd');
SELECT  * from type_char  where string1 SIMILAR TO 'a{0}bababcd';
DROP TABLE IF EXISTS type_char;