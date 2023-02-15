-- @testpoint: 验证原语法和MySQL兼容语法hash分区增删分区(segment=on)，部分场景合理报错

-- 原语法
drop table if exists t_b_add_drop_par_0039;
create table t_b_add_drop_par_0039(c1 int,c2 int)
with (segment=on)
partition by hash(c1) (
  partition p1,
  partition p2,
  partition p3
  );
create index i_b_add_drop_par_0039_1 on t_b_add_drop_par_0039 (c1) global;
create index i_b_add_drop_par_0039_2 on t_b_add_drop_par_0039 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039')) order by relname;

-- 添加一个分区报错
alter table t_b_add_drop_par_0039 add partition p4;
alter table t_b_add_drop_par_0039 add partition p4 values(1);
-- 添加多个分区报错
alter table t_b_add_drop_par_0039 add partition p5,add partition p6;
alter table t_b_add_drop_par_0039 add partition p5 values(1),add partition p6 values(1);
-- 指定表空间为pg_global报错
alter table t_b_add_drop_par_0039 add partition p6 tablespace pg_global;
alter table t_b_add_drop_par_0039 add partition p6 values(1) tablespace pg_global;
-- 删除一个分区报错
alter table t_b_add_drop_par_0039 drop partition p1;
-- 删除多个分区报错
alter table t_b_add_drop_par_0039 drop partition p2,drop partition p3;
-- 删除不存在的分区报错
alter table t_b_add_drop_par_0039 drop partition p6;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039')) order by relname;
-- 清理环境
drop table t_b_add_drop_par_0039;

-- MySQL兼容语法
drop table if exists t_b_add_drop_par_0039;
create table t_b_add_drop_par_0039(c1 int,c2 int)
with (segment=on)
partition by hash(c1) (
  partition p1,
  partition p2,
  partition p3
  );
create index i_b_add_drop_par_0039_3 on t_b_add_drop_par_0039 (c1) global;
create index i_b_add_drop_par_0039_4 on t_b_add_drop_par_0039 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039')) order by relname;

-- 添加一个分区报错
alter table t_b_add_drop_par_0039 add partition (partition  p4);
alter table t_b_add_drop_par_0039 add partition (partition  p4 values(1));
-- 添加多个分区报错
alter table t_b_add_drop_par_0039 add partition (partition p5,partition p6);
alter table t_b_add_drop_par_0039 add partition (partition p5 values(1),partition p6 values(1));
-- 指定表空间为pg_global报错
alter table t_b_add_drop_par_0039 add partition (partition p6 tablespace pg_global);
alter table t_b_add_drop_par_0039 add partition (partition p6 values(1) tablespace pg_global);
-- 删除一个分区报错
alter table t_b_add_drop_par_0039 drop partition p1;
-- 删除多个分区报错
alter table t_b_add_drop_par_0039 drop partition p2,p3;
-- 删除不存在的分区报错
alter table t_b_add_drop_par_0039 drop partition p6;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0039')) order by relname;
-- 清理环境
drop table t_b_add_drop_par_0039;
