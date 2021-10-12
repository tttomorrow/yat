-- @testpoint: 中文字符颠倒
drop database if exists logdb;
create database logdb encoding='UTF8';
select col1 from wdr_xdb_query('dbname=logdb','select reverse(''中国123中文字符颠倒'')') as dd(col1 varchar);
drop database if exists logdb;