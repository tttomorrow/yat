-- @testpoint: 模式匹配POSIX正则表达式,使用{m,n}重复前面的项至少m次并且不超过n次去匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('aabc');
SELECT * from type_char  where string1 ~ 'a{1,3}(b|c)';
DROP TABLE IF EXISTS type_char;