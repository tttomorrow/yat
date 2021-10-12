-- @testpoint: 参数为二进制
DROP TABLE IF EXISTS type_binary;
CREATE TABLE type_binary (string1 text);
insert into type_binary values (quote_nullable('DEADBEEF'::raw));
SELECT * from type_binary;
DROP TABLE IF EXISTS type_binary;