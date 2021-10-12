-- @testpoint: 参数g不使用
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('hello world');
SELECT regexp_split_to_table(string1,'wo') from type_char;
select * from type_char;
DROP TABLE IF EXISTS type_char;