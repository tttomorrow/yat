-- @testpoint: 模式匹配POSIX正则表达式,使用{m}重复前面的项刚好m次去匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('aaabc');
SELECT * from type_char  where string1 ~ 'a{3}(b|c)';
DROP TABLE IF EXISTS type_char;