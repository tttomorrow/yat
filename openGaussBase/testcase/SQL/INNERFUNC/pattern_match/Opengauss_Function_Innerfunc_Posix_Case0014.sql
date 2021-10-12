-- @testpoint: 模式匹配POSIX正则表达式,对元字符$进行匹配
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 varchar(100));
insert into type_char values ('@1$');
SELECT * from type_char  where string1 ~ '@1[$]';
DROP TABLE IF EXISTS type_char;