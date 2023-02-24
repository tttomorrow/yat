-- @testpoint: 验证原语法和MySQL兼容语法list分区增加分区(主表指定非默认tablespace)，部分场景合理报错
-- 原语法
drop tablespace if exists ts_b_add_drop_par_0032;
create tablespace ts_b_add_drop_par_0032 relative location 'ts_b_add_drop_par_0032';
drop table if exists t_b_add_drop_par_0032;
create table t_b_add_drop_par_0032(c1 int primary key,c2 int,c3 int)
tablespace ts_b_add_drop_par_0032
partition by list(c3) (
  partition p1 values(1),
  partition p2 values(2),
  partition p3 values(3)
  );
create index i_b_add_drop_par_0032_1 ON t_b_add_drop_par_0032 (c1) global;
create index i_b_add_drop_par_0032_2 ON t_b_add_drop_par_0032 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032')) order by relname;

-- 添加一个分区成功
alter table t_b_add_drop_par_0032 add partition p4 values (4);
-- 添加多个分区成功
alter table t_b_add_drop_par_0032 add partition p5 values (5),add partition p6 values (6);
-- 添加重名分区报错
alter table t_b_add_drop_par_0032 add partition p6 values (7);
-- 添加非法分区报错
alter table t_b_add_drop_par_0032 add partition p7 values (1);
-- 添加与分区键不同类型分区报错
alter table t_b_add_drop_par_0032 add partition p8 values ('a');
-- 指定表空间成功
alter table t_b_add_drop_par_0032 add partition p7 values (7) tablespace ts_b_add_drop_par_0032;
-- 指定表空间为pg_global报错
alter table t_b_add_drop_par_0032 add partition p8 values (8) tablespace pg_global;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0032;

-- MySQL兼容语法
drop table if exists t_b_add_drop_par_0032;
create table t_b_add_drop_par_0032(c1 int primary key,c2 int,c3 int)
tablespace ts_b_add_drop_par_0032
partition by list(c3) (
  partition p1 values(1),
  partition p2 values(2),
  partition p3 values(3)
  );
create index i_b_add_drop_par_0032_3 ON t_b_add_drop_par_0032 (c1) global;
create index i_b_add_drop_par_0032_4 ON t_b_add_drop_par_0032 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032')) order by relname;

-- 添加一个分区成功
alter table t_b_add_drop_par_0032 add partition (partition p4 values (4));
-- 添加多个分区成功
alter table t_b_add_drop_par_0032 add partition (partition p5 values (5),partition p6 values (6));
-- 添加重名分区报错
alter table t_b_add_drop_par_0032 add partition (partition p6 values (7));
-- 添加非法分区报错
alter table t_b_add_drop_par_0032 add partition (partition p7 values (1));
-- 添加与分区键不同类型分区报错
alter table t_b_add_drop_par_0032 add partition (partition p8 values ('a'));
-- 指定表空间成功
alter table t_b_add_drop_par_0032 add partition (partition p7 values (7) tablespace ts_b_add_drop_par_0032);
-- 指定表空间为pg_global报错
alter table t_b_add_drop_par_0032 add partition (partition p8 values (8) tablespace pg_global);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0032')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0032;
drop tablespace ts_b_add_drop_par_0032;

