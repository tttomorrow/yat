-- @testpoint: 行存表列约束default,unique,foreign key的同时创建唯一索引,合理报错

--1.创建行存一般表
create table foreign_key_table(i int unique);
create table main_table(i int,c varchar default 'rr',x int references foreign_key_table(i),unique(i));
--2.在各列上创建唯一索引
create unique index i_idx on main_table(i);
create unique index c_idx on main_table(c);
create unique index x_idx on main_table(x);
--3.插入数据
insert into main_table values(1,'dd'),(1,'ee');
insert into main_table values(2),(3);
insert into main_table values(4,'dd2',1),(5,'e2e',1);
--4.查看索引
SET ENABLE_SEQSCAN=off;
explain select i from main_table;
explain select c from main_table;
explain select x from main_table;
--5.创建本地临时表
create local temp table foreign_key_table_local(i int unique);
create local temp table main_table_local(i int,c varchar default 'rr',x int references foreign_key_table_local(i),unique(i));
--6.在各列上创建唯一索引
create unique index i_idx_local on main_table_local(i);
create unique index c_idx_local on main_table_local(c);
create unique index x_idx_local on main_table_local(x);
--7.插入数据
insert into main_table_local values(1,'dd'),(1,'ee');
insert into main_table_local values(2),(3);
insert into main_table_local values(4,'dd2',1),(5,'e2e',1);
--8.查看索引
SET ENABLE_SEQSCAN=off;
explain select i from main_table_local;
explain select c from main_table_local;
explain select x from main_table_local;
--9.创建全局临时表
create global temp table foreign_key_table_global(i int unique);
create global temp table main_table_global(i int,c varchar default 'rr',x int references foreign_key_table_global(i),unique(i));
--10.在各列上创建唯一索引
create unique index i_idx_global on main_table_global(i);
create unique index c_idx_global on main_table_global(c);
create unique index x_idx_global on main_table_global(x);
--11.插入数据
insert into main_table_global values(1,'dd'),(1,'ee');
insert into main_table_global values(2),(3);
insert into main_table_global values(4,'dd2',1),(5,'e2e',1);
--12.查看索引
SET ENABLE_SEQSCAN=off;
explain select i from main_table_global;
explain select c from main_table_global;
explain select x from main_table_global;

--tearDown
drop table if exists foreign_key_table cascade;
drop table if exists main_table cascade;
drop table if exists foreign_key_table_local cascade;
drop table if exists main_table_local cascade;
drop table if exists foreign_key_table_global cascade;
drop table if exists main_table_global cascade;
