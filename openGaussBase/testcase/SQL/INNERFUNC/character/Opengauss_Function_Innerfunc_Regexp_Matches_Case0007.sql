-- @testpoint: [A-z的使用]
DROP TABLE IF EXISTS type_char;
CREATE TABLE type_char (string1 char(100));
insert into type_char values ('fooBarbequebazilbarfbonk');
SELECT regexp_matches(string1,'[A-z]','g') from type_char;
DROP TABLE IF EXISTS type_char;