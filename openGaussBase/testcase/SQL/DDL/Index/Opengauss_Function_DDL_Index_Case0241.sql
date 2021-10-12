-- @testpoint: 分区表列约束default,unique,foreign key的同时创建唯一索引,合理报错

-- 1.创建分区表
create table foreign_key_table(i int unique) partition by range(i) (partition p1 values less than(10));
create table foreign_key_table1(i int unique);
CREATE TABLE hash_tb(i int,c varchar default 'rr',x int references foreign_key_table(i)) PARTITION BY hash (i)(partition h1, partition h2);
CREATE TABLE range_tb(i int,c varchar default 'rr',x int references foreign_key_table(i)) PARTITION BY range(x)(partition p1 values less than(10),partition p2 values less than(maxvalue));
CREATE TABLE list_tb(i int,c varchar default 'rr',x int references foreign_key_table1(i)) PARTITION BY list(x) (partition p1_list values (10,20), partition p1_list1 values(30,40));
-- 2.创建唯一索引
create unique index i_idx on hash_tb(i);
create unique index x_range_idx on range_tb(x);
create unique index x_list_idx on list_tb(x);
-- 3.插入数据
insert into hash_tb values(1,'dd'),(1,'ee');
insert into hash_tb values(generate_series(10,90000));
insert into range_tb values(2,'asd',2),(2,'ddd',2);
insert into foreign_key_table1 values (10);
insert into list_tb values(4,'dd2',10),(5,'e2e',10);
-- 4.查看索引
SET ENABLE_SEQSCAN=off;
explain select i from  hash_tb;
explain select x from range_tb;
explain select x from list_tb;

--tearDown
drop table if exists hash_tb cascade;
drop table if exists foreign_key_table cascade;
drop table if exists foreign_key_table1 cascade;
drop table if exists range_tb cascade;
drop table if exists list_tb cascade;
