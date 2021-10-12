-- @testpoint: 带逃逸字符匹配不到
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('Thomas');
SELECT substring(string1 from  '%#"o_s#"_' for '#') from type_char;
DROP TABLE IF EXISTS type_char;