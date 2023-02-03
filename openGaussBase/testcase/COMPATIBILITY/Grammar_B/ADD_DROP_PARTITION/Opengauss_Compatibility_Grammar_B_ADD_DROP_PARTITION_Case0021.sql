-- @testpoint: 验证原语法和MySQL兼容语法range分区增加分区(segment=on)，部分场景合理报错

-- 原语法
drop tablespace if exists ts_b_add_drop_par_0021;
create tablespace ts_b_add_drop_par_0021 relative location 'ts_b_add_drop_par_0021';
drop table if exists t_b_add_drop_par_0021;
create table t_b_add_drop_par_0021(c1 int primary key,c2 int)
with (segment=on)
partition by range(c1) (
  partition p1 values less than(100),
  partition p2 values less than(200),
  partition p3 values less than(300)
  );
create index i_b_add_drop_par_0021_1 on t_b_add_drop_par_0021 (c2) global;
create index i_b_add_drop_par_0021_2 on t_b_add_drop_par_0021 (c1) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021')) order by relname;

-- 添加一个分区成功
alter table t_b_add_drop_par_0021 add partition p4 values less than(400);
-- 添加多个分区成功
alter table t_b_add_drop_par_0021 add partition p5 values less than(500),add partition p6 values less than(600);
-- 添加重名分区报错
alter table t_b_add_drop_par_0021 add partition p6 values less than(700);
-- 添加非法分区报错
alter table t_b_add_drop_par_0021 add partition p7 values less than(10);
-- 添加与分区键不同类型分区报错
alter table t_b_add_drop_par_0021 add partition p8 values less than('a');
-- 指定表空间成功
alter table t_b_add_drop_par_0021 add partition p7 values less than(700) tablespace ts_b_add_drop_par_0021;
-- 指定表空间为pg_global报错
alter table t_b_add_drop_par_0021 add partition p8 values less than(800) tablespace pg_global;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021')) order by relname;
-- 清理环境
drop table t_b_add_drop_par_0021;

-- MySQL兼容语法
drop table if exists t_b_add_drop_par_0021;
create table t_b_add_drop_par_0021(c1 int primary key,c2 int)
with (segment=on)
partition by range(c1) (
  partition p1 values less than(100),
  partition p2 values less than(200),
  partition p3 values less than(300)
  );
create index i_b_add_drop_par_0021_3 on t_b_add_drop_par_0021 (c2) global;
create index i_b_add_drop_par_0021_4 on t_b_add_drop_par_0021 (c1) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021')) order by relname;

-- 添加一个分区成功
alter table t_b_add_drop_par_0021 add partition (partition p4 values less than(400));
-- 添加多个分区成功
alter table t_b_add_drop_par_0021 add partition (partition p5 values less than(500),partition p6 values less than(600));
-- 添加重名分区报错
alter table t_b_add_drop_par_0021 add partition (partition p6 values less than(700));
-- 添加非法分区报错
alter table t_b_add_drop_par_0021 add partition (partition p7 values less than(10));
-- 添加与分区键不同类型分区报错
alter table t_b_add_drop_par_0021 add partition (partition p8 values less than('a'));
-- 指定表空间成功
alter table t_b_add_drop_par_0021 add partition (partition p7 values less than(700) tablespace ts_b_add_drop_par_0021);
-- 指定表空间为pg_global报错
alter table t_b_add_drop_par_0021 add partition (partition p8 values less than(800) tablespace pg_global);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0021')) order by relname;
-- 清理环境
drop table t_b_add_drop_par_0021;
drop tablespace ts_b_add_drop_par_0021;
