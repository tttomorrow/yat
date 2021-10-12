-- @testpoint: 只有一个单词
-- @modify at: 2020-11-16
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('j');
SELECT initcap(string1) from type_char;
DROP TABLE IF EXISTS type_char;