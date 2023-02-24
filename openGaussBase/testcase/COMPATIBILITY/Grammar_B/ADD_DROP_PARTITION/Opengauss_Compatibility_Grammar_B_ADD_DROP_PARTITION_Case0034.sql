-- @testpoint: 验证原语法和MySQL兼容语法list分区删除分区(ustore)，部分场景合理报错

-- 原语法
drop table if exists t_b_add_drop_par_0034;
create table t_b_add_drop_par_0034(c1 int primary key,c2 int,c3 int)
with (storage_type=ustore)
partition by list(c3) (
  partition p1 values(1),
  partition p2 values(2),
  partition p3 values(3),
  partition p4 values(4),
  partition p5 values(5)
  );
create index i_b_add_drop_par_0034_1 ON t_b_add_drop_par_0034 (c1) global;
create index i_b_add_drop_par_0034_2 ON t_b_add_drop_par_0034 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034')) order by relname;

-- 删除一个分区成功
alter table t_b_add_drop_par_0034 drop partition p1;
-- 删除多个分区成功
alter table t_b_add_drop_par_0034 drop partition p2,drop partition p3,drop partition p4;
-- 删除最后一个分区报错
alter table t_b_add_drop_par_0034 drop partition p5;
-- 删除不存在的分区报错
alter table t_b_add_drop_par_0034 drop partition p6;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0034;

-- MySQL兼容语法
drop table if exists t_b_add_drop_par_0034;
create table t_b_add_drop_par_0034(c1 int primary key,c2 int,c3 int)
with (storage_type=ustore)
partition by list(c3) (
  partition p1 values(1),
  partition p2 values(2),
  partition p3 values(3),
  partition p4 values(4),
  partition p5 values(5)
  );
create index i_b_add_drop_par_0034_3 ON t_b_add_drop_par_0034 (c1) global;
create index i_b_add_drop_par_0034_4 ON t_b_add_drop_par_0034 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034')) order by relname;

-- 删除一个分区成功
alter table t_b_add_drop_par_0034 drop partition p1;
-- 删除多个分区成功
alter table t_b_add_drop_par_0034 drop partition p2,p3,p4;
-- 删除最后一个分区报错
alter table t_b_add_drop_par_0034 drop partition p5;
-- 删除不存在的分区报错
alter table t_b_add_drop_par_0034 drop partition p6;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0034')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0034;

