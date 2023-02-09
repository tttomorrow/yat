-- @testpoint: 验证间隔分区表增删分区原语法和MySQL兼容语法
-- 指定表空间
drop tablespace if exists ts_b_add_drop_par_0016;
create tablespace ts_b_add_drop_par_0016 relative location 'ts_b_add_drop_par_0016';
drop table if exists t_b_add_drop_par_0016;
create table t_b_add_drop_par_0016(c1 int primary key,c2 timestamp)
tablespace ts_b_add_drop_par_0016
partition by range(c2)
interval('1 day')
(
  partition p1 values less than ('1990-01-01 00:00:00'),
  partition p2 values less than ('1990-01-02 00:00:00'),
  partition p3 values less than ('1990-01-03 00:00:00'),
  partition p4 values less than ('1990-01-04 00:00:00'),
  partition p5 values less than ('1990-01-05 00:00:00'),
  partition p6 values less than ('1990-01-06 00:00:00'),
  partition p7 values less than ('1990-01-07 00:00:00'),
  partition p8 values less than ('1990-01-08 00:00:00'),
  partition p9 values less than ('1990-01-09 00:00:00'),
  partition p10 values less than ('1990-01-10 00:00:00')
) ;
create index i_b_add_drop_par_0016_1 on t_b_add_drop_par_0016 (c1) global;
create index i_b_add_drop_par_0016_2 on t_b_add_drop_par_0016 (c2) local;
insert into t_b_add_drop_par_0016 values
  (1,'1990-01-01 00:00:00'),
  (2,'1990-01-02 00:00:00'),
  (3,'1990-01-03 00:00:00'),
  (4,'1990-01-04 00:00:00'),
  (5,'1990-01-05 00:00:00');
select relname,boundaries from pg_partition where parentid in (select oid from pg_class where relname = 't_b_add_drop_par_0016') order by relname;
-- MySQL语法 drop partition
alter table t_b_add_drop_par_0016 drop partition p1;
alter table t_b_add_drop_par_0016 drop partition p2,p3;
-- @testpoint: 删除全部分区，合理报错
alter table t_b_add_drop_par_0016 drop partition p4,p5,p6,p7,p8,p9,p10;
alter table t_b_add_drop_par_0016 drop partition p4,p5,p6,p7,p8,p9;
-- @testpoint: 删除最后一个分区，合理报错
alter table t_b_add_drop_par_0016 drop partition p10;
-- @testpoint: 删除不存在的分区，合理报错
alter table t_b_add_drop_par_0016 drop partition p1;
select relname,boundaries from pg_partition where parentid in (select oid from pg_class where relname = 't_b_add_drop_par_0016') order by relname;
drop table t_b_add_drop_par_0016;
-- 重新建表
create table t_b_add_drop_par_0016(c1 int primary key,c2 timestamp)
tablespace ts_b_add_drop_par_0016
partition by range(c2)
interval('1 day')
(
  partition p1 values less than ('1990-01-01 00:00:00'),
  partition p2 values less than ('1990-01-02 00:00:00'),
  partition p3 values less than ('1990-01-03 00:00:00'),
  partition p4 values less than ('1990-01-04 00:00:00'),
  partition p5 values less than ('1990-01-05 00:00:00'),
  partition p6 values less than ('1990-01-06 00:00:00'),
  partition p7 values less than ('1990-01-07 00:00:00'),
  partition p8 values less than ('1990-01-08 00:00:00'),
  partition p9 values less than ('1990-01-09 00:00:00'),
  partition p10 values less than ('1990-01-10 00:00:00')
) ;
create index i_b_add_drop_par_0016_3 on t_b_add_drop_par_0016 (c1) global;
create index i_b_add_drop_par_0016_4 on t_b_add_drop_par_0016 (c2) local;
insert into t_b_add_drop_par_0016 values
  (1,'1990-01-01 00:00:00'),
  (2,'1990-01-02 00:00:00'),
  (3,'1990-01-03 00:00:00'),
  (4,'1990-01-04 00:00:00'),
  (5,'1990-01-05 00:00:00');
select relname,boundaries from pg_partition where parentid in (select oid from pg_class where relname = 't_b_add_drop_par_0016') order by relname;
-- 原语法 drop partition
alter table t_b_add_drop_par_0016 drop partition p1;
alter table t_b_add_drop_par_0016 drop partition p2,drop partition p3;
-- @testpoint: 删除全部分区，合理报错
alter table t_b_add_drop_par_0016 drop partition p4,drop partition p5,drop partition p6,drop partition p7,drop partition p8,drop partition p9,drop partition p10;
alter table t_b_add_drop_par_0016 drop partition p4,drop partition p5,drop partition p6,drop partition p7,drop partition p8,drop partition p9;
-- @testpoint: 删除最后一个分区，合理报错
alter table t_b_add_drop_par_0016 drop partition p10;
-- @testpoint: 删除不存在的分区，合理报错
alter table t_b_add_drop_par_0016 drop partition p1;
select relname,boundaries from pg_partition where parentid in (select oid from pg_class where relname = 't_b_add_drop_par_0016') order by relname;
drop table t_b_add_drop_par_0016;
drop tablespace ts_b_add_drop_par_0016;
