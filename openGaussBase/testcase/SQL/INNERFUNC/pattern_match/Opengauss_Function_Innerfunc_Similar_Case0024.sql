-- @testpoint: 模式匹配操作符SIMILAR TO,使用元字符{m,} ,重复前面的项至少m次去匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('ababbababcd');
SELECT  * from type_char  where string1 SIMILAR TO '(ab){2,}bababcd';
DROP TABLE IF EXISTS type_char;