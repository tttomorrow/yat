-- @testpoint: 验证原语法和MySQL兼容语法range分区删除分区，部分场景合理报错

-- 原语法
drop table if exists t_b_add_drop_par_0023;
create table t_b_add_drop_par_0023(c1 int primary key,c2 int)
partition by range(c1) (
  partition p1 values less than(100),
  partition p2 values less than(200),
  partition p3 values less than(300),
  partition p4 values less than(400),
  partition p5 values less than(500)
  );
create index i_b_add_drop_par_0023_1 on t_b_add_drop_par_0023 (c2) global;
create index i_b_add_drop_par_0023_2 on t_b_add_drop_par_0023 (c1) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023')) order by relname;

-- 删除一个分区成功
alter table t_b_add_drop_par_0023 drop partition p1;
-- 删除多个分区成功
alter table t_b_add_drop_par_0023 drop partition p2,drop partition p3,drop partition p4;
-- 删除最后一个分区报错
alter table t_b_add_drop_par_0023 drop partition p5;
-- 删除不存在的分区报错
alter table t_b_add_drop_par_0023 drop partition p6;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023')) order by relname;
-- 清理环境
drop table t_b_add_drop_par_0023;

-- MySQL兼容语法
drop table if exists t_b_add_drop_par_0023;
create table t_b_add_drop_par_0023(c1 int primary key,c2 int)
partition by range(c1) (
  partition p1 values less than(100),
  partition p2 values less than(200),
  partition p3 values less than(300),
  partition p4 values less than(400),
  partition p5 values less than(500)
  );
create index i_b_add_drop_par_0023_3 on t_b_add_drop_par_0023 (c2) global;
create index i_b_add_drop_par_0023_4 on t_b_add_drop_par_0023 (c1) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023')) order by relname;

-- 删除一个分区成功
alter table t_b_add_drop_par_0023 drop partition p1;
-- 删除多个分区成功
alter table t_b_add_drop_par_0023 drop partition p2,p3,p4;
-- 删除最后一个分区报错
alter table t_b_add_drop_par_0023 drop partition p5;
-- 删除不存在的分区报错
alter table t_b_add_drop_par_0023 drop partition p6;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0023')) order by relname;
-- 清理环境
drop table t_b_add_drop_par_0023;
