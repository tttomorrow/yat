-- @testpoint: 创建索引使用不同索引名称,合理报错

-- 1.创建表
drop table if exists test;
create table test(i int, c char(5));
-- 2.创建索引，索引名以字母开头
create unique index unique_123idx on test(i,c);
--3.创建索引，索引名以下划线开头
create unique index _123$idx on test(i,c);
--4.创建索引，索引名为数字
create index 123 on test(i);
--5.创建索引，索引名为数字开头
create index 1_idx on test(i);
--6.创建索引，索引名包含特殊符号
create index a%idx on test(i);
--7.创建schema
drop schema if exists new_schema cascade;
create schema new_schema create table sc_tb(i int);
drop schema if exists test_schema cascade;
create schema test_schema;
create index test_schema.schema_idx on new_schema.sc_tb(i);

--tearDown
drop table if exists new_schema.sc_tb cascade;
drop table if exists test cascade;
drop schema if exists new_schema cascade;
drop schema if exists test_schema cascade;
