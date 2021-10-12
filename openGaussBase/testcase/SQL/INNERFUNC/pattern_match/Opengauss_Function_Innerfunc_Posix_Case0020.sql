-- @testpoint: 模式匹配POSIX正则表达式,使用?匹配由原子的0次或1次匹配组成的序列
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('aabc');
SELECT * from type_char  where string1 ~ 'a?(b|c)';
DROP TABLE IF EXISTS type_char;