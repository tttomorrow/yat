-- @testpoint: 索引列明存在或不存在表中,合理报错

--1. 创建表
create table test_tb(id int, date_time date);
--2.插入数据
insert into test_tb values(generate_series(1,2000), '2021-04-01') ;
--3.创建索引，索引列名不存在
create index t_idx on test_tb(not);
--4.创建索引，索引列名存在
create index t_idx on test_tb(id);
--5.创建索引，无列名
create index id_idx on test_tb;

--tearDown
drop table if exists test_tb cascade;