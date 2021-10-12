-- @testpoint: 中文
drop database if exists logdb;
create database logdb encoding='UTF8';

select col1 from wdr_xdb_query('dbname=logdb',
'CREATE TABLE type_char (string1 char(100));
insert into type_char values (''我是一个'');') as dd(col1 varchar);

select col1 from wdr_xdb_query('dbname=logdb',
'SELECT substrb(string1,2,6) from type_char;') as dd(col1 varchar);

select col1 from wdr_xdb_query('dbname=logdb',
'SELECT substrb(string1,4,9) from type_char;') as dd(col1 varchar);

drop database if exists logdb;