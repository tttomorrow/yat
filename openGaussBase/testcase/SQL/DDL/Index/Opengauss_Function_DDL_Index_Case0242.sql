-- @testpoint: 创建 gist索引,合理报错

--1.创建表
create table table_gist(p point, c1  point, c2  point, i int);
create table table_gist_exp(c circle, i int);
--2.创建gist索引
create index part_idx on table_gist using gist(p) where p <^ point(1,2);
create index team_idx on table_gist using gist(p) where c1 <^ point(1,2) and c2 >^ point(3,10);
create index exp_idx on table_gist_exp using gist(point(c));
--3.插入数据
insert into table_gist values(point(0,0),point(0,0),point(0,0),generate_series(1,20000));
insert into table_gist values(point(2,2),point(0,0),point(4,20), generate_series(20001,40000));
insert into table_gist_exp values(circle'((1,2), 3)', generate_series(1,400));
insert into table_gist_exp values(circle'((1,2), 2)', generate_series(3000,4000));
--4.查看索引
SET ENABLE_SEQSCAN=off;
explain select * from table_gist where p<^ point(1,2);
explain select * from table_gist where c1 <^ point(1,2) and c2 >^ point(3,10);
explain select * from  table_gist_exp where point(c)>^ point(1,1);
--5.查看查询结果
select count(*) from table_gist where p<^ point(1,2);
select count(*) from table_gist where c1 <^ point(1,2) and c2 >^ point(3,10);
select  count(*) from  table_gist_exp where point(c)>^ point(1,1);
--6.创建临时表
create temp table table_gist_tmp(p point, c1  point, c2  point, i int);
create global temp table table_gist_tmp_global(p point, c1  point, c2  point, i int);
create temp table table_gist_exp_tmp(c circle, i int);
create global temp table table_gist_exp_tmp_global(c circle, i int);
--7.创建gist索引
create index part_idx_temp on table_gist_tmp using gist(p) where p <^ point(1,2);
create index team_idx_temp on table_gist_tmp using gist(p) where c1 <^ point(1,2) and c2 >^ point(3,10);
create index part_idx_temp_gloabl on table_gist_tmp_global using gist(p) where p <^ point(1,2);
create index team_idx_temp_gloabl on table_gist_tmp_global using gist(p) where c1 <^ point(1,2) and c2 >^ point(3,10);
create index exp_idx_tmp on table_gist_exp_tmp using gist(point(c));
create index exp_idx_tmp_global on table_gist_exp_tmp_global using gist(point(c));
--8.插入数据
insert into table_gist_tmp values(point(0,0),point(0,0),point(0,0),generate_series(1,20000));
insert into table_gist_tmp values(point(2,2),point(0,0),point(4,20), generate_series(20001,40000));
insert into table_gist_tmp_global values(point(0,0),point(0,0),point(0,0),generate_series(1,20000));
insert into table_gist_tmp_global values(point(2,2),point(0,0),point(4,20), generate_series(20001,40000));
insert into table_gist_exp_tmp values(circle'((1,2), 3)', generate_series(1,400));
insert into table_gist_exp_tmp_global values(circle'((1,2), 3)', generate_series(1,400));
--9.查看索引
SET ENABLE_SEQSCAN=off;
explain select * from table_gist_tmp where p<^ point(1,2);
explain select * from table_gist_tmp where c1 <^ point(1,2) and c2 >^ point(3,10);
explain select * from table_gist_tmp_global where p<^ point(1,2);
explain select * from table_gist_tmp_global where c1 <^ point(1,2) and c2 >^ point(3,10);
explain select * from  table_gist_exp_tmp where point(c)>^ point(1,1);
explain select * from  table_gist_exp_tmp_global where point(c)>^ point(1,1);
--10.查看查询结果
select count(*) from table_gist_tmp where p<^ point(1,2);
select count(*) from table_gist_tmp where c1 <^ point(1,2) and c2 >^ point(3,10);
select count(*) from  table_gist_tmp_global where p<^ point(1,2);
select count(*) from  table_gist_tmp_global where c1 <^ point(1,2) and c2 >^ point(3,10);
select count(*) from  table_gist_exp_tmp where point(c)>^ point(1,1);
select count(*) from  table_gist_exp_tmp_global where point(c)>^ point(1,1);

--tearDown
drop table if exists table_gist_exp cascade;
drop table if exists table_gist cascade;
drop table if exists table_gist_exp_tmp cascade;
drop table if exists table_gist_exp_tmp_global cascade;
drop table if exists table_gist_tmp_global cascade;
drop table if exists table_gist_tmp cascade;
drop table if exists table_gist_tmp_global cascade;