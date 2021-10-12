-- @testpoint: 中文
drop database if exists logdb;
create database logdb encoding='UTF8';
select col1 from wdr_xdb_query('dbname=logdb',
'SELECT regexp_substr(''我是'',''[我]'');') as dd(col1 varchar);
select col1 from wdr_xdb_query('dbname=logdb',
'CREATE TABLE type_char (string1 char(100));
insert into type_char values (''我是'');
SELECT regexp_substr(string1,''[我]'') from type_char;') as dd(col1 varchar);
drop database if exists logdb;