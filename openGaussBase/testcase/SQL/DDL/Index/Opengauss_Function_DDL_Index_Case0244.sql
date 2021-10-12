-- @testpoint: 行存表创建btree索引,合理报错

--1.创建表
create table normal_tb(i int, name varchar);
--2.插入数据
insert into normal_tb values(generate_series(1,1000), 'test');
insert into normal_tb values(generate_series(9999,10530), 'ytest');
--3.创建索引
create index exp_idx on normal_tb using btree(upper(name));
--4.查询索引
SET ENABLE_SEQSCAN=off;
explain select * from normal_tb where upper(name)='TEST';
--5.查询数据
select count(*) from normal_tb where upper(name)='TEST';
--6.创建临时表
create local temp table tmp_tb(i int, name varchar);
create global temp table global_tmp_tb(i int, name varchar);
--7.插入数据
insert into tmp_tb values(generate_series(1,1000), 'test');
insert into global_tmp_tb values(generate_series(9999,10530), 'ytest');
--8.创建索引
create index part_idx_tmp on tmp_tb using btree(i) where i>100;
create index exp_idx_tmp on tmp_tb using btree(upper(name));
create index team_idx_tmp_gloabl on global_tmp_tb using btree(i,name) ;
create index part_idx_tmp_gloabl on global_tmp_tb using btree(i) where i>100;
create index exp_idx_tmp_gloabl on global_tmp_tb using btree(upper(name));
--9.查询索引
SET ENABLE_SEQSCAN=off;
explain select * from tmp_tb where i> 500;
explain select * from tmp_tb where upper(name)='TEST';
explain select * from global_tmp_tb where i> 500;
explain select * from global_tmp_tb where upper(name)='TEST';
explain select * from global_tmp_tb where upper(name)='TEST' and i <300;

--10.查询表
select count(*) from tmp_tb where i> 500;
select count(*) from tmp_tb where upper(name)='TEST';
select count(*) from tmp_tb where i>300 and name='test';
select count(*) from global_tmp_tb where i> 500;
select count(*) from global_tmp_tb where upper(name)='TEST';
select count(*) from global_tmp_tb where name='TEST' and i <300;
--11.创建分区表
create table tb_btree_partition(id int,name varchar)
PARTITION BY RANGE(id)(
        PARTITION P1 VALUES LESS THAN(100),
        PARTITION P2 VALUES LESS THAN(1000),
        PARTITION P3 VALUES LESS THAN(MAXVALUE))
;
--12.插入数据
insert into tb_btree_partition values(generate_series(1,1000), 'testd');
--13.创建索引
create index part_idx on tb_btree_partition using btree(id) local (partition p1, partition p2, partition p3) where id>500;
create index team_idx_global on tb_btree_partition using btree(id, name) global;
--14.查询索引
SET ENABLE_SEQSCAN=off;
explain select * from tb_btree_partition where i> 500;
explain select * from tb_btree_partition where upper(name)='TEST';

--tearDown
drop table if exists normal_tb cascade;
drop table if exists tmp_tb cascade;
drop table if exists tb_btree_partition cascade;
drop table if exists global_tmp_tb cascade;
