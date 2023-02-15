-- @testpoint: 验证MySQL兼容语法hash-hash分区表增删分区(ustore)，部分场景合理报错

drop tablespace if exists ts_b_add_drop_par_0108;
create tablespace ts_b_add_drop_par_0108 relative location 'ts_b_add_drop_par_0108';
drop table if exists t_b_add_drop_par_0108;
create table t_b_add_drop_par_0108(c1 int primary key,c2 int,c3 int)
with (storage_type=ustore)
partition by hash(c1) subpartition by hash(c2) 
(
  partition p1
  (
    subpartition p1_1,
    subpartition p1_2
  ),
  partition p2
  (
    subpartition p2_1,
    subpartition p2_2
  )
);
create index i_b_add_drop_par_0108_1 on t_b_add_drop_par_0108 (c1) global;
create index i_b_add_drop_par_0108_2 on t_b_add_drop_par_0108 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0108') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0108')) order by relname;

-- 非法添加一级二级分区报错
-- 添加一级分区不指定二级子分区
alter table t_b_add_drop_par_0108 add partition (partition p3 values less than(300));
-- 添加一级分区指定一个二级分区
alter table t_b_add_drop_par_0108 add partition (partition p4 values less than(400) (subpartition p4_1 values less than(400)));
-- 添加一级分区指定多个二级分区
alter table t_b_add_drop_par_0108 add partition (partition p5 values less than(500) (subpartition p5_1 values less than(450),subpartition p5_2 values less than(500)));
-- 添加多个一级分区
alter table t_b_add_drop_par_0108 add partition (partition p6 values less than(600) (subpartition p6_1 values less than(510)),partition p7 values less than(700));
-- 为一级分区添加一个子分区
alter table t_b_add_drop_par_0108 modify partition p2 add subpartition p2_3 values less than(520);
-- 为一级分区添加多个子分区
alter table t_b_add_drop_par_0108 modify partition p2 add subpartition p2_3 values less than(530),modify partition p2 add subpartition p2_4 values less than(540);
-- 添加一级分区指定表空间
alter table t_b_add_drop_par_0108 add partition (partition p8 values less than(800) tablespace ts_b_add_drop_par_0108);
-- 添加二级分区指定表空间
alter table t_b_add_drop_par_0108 modify partition p2 add subpartition p2_5 values less than(550) tablespace ts_b_add_drop_par_0108;
-- 分区重名
alter table t_b_add_drop_par_0108 add partition (partition p2 values less than(900));
-- 一级分区值非法
alter table t_b_add_drop_par_0108 add partition (partition p9 values less than(100));
-- 一级分区值合法，二级分区值非法
alter table t_b_add_drop_par_0108 add partition (partition p9 values less than(900) (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50)));
-- 一级分区值非法，二级分区值合法
alter table t_b_add_drop_par_0108 add partition (partition p9 values less than(100) (subpartition p9_1 values less than(100),subpartition p9_2 values less than(200)));
-- 一级分区值非法，二级分区值非法
alter table t_b_add_drop_par_0108 add partition (partition p9 values less than(100) (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50)));
-- 一级分区数据类型非法
alter table t_b_add_drop_par_0108 add partition (partition p9 values less than('a') (subpartition p9_1 values less than(100)));
-- 二级分区值非法
alter table t_b_add_drop_par_0108 add partition (partition p9 values less than(900) (subpartition p9_1 values less than('a')));
-- 一级分区指定表空间为pg_global
alter table t_b_add_drop_par_0108 add partition (partition p8 values less than(900) tablespace pg_global);
-- 二级分区指定表空间为pg_global
alter table t_b_add_drop_par_0108 add partition (partition p9 values less than(900) (subpartition p9_1 values less than(100) tablespace pg_global));

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0108') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0108')) order by relname;

-- 非法删除分区报错
-- 删除一个一级分区
alter table t_b_add_drop_par_0108 drop partition p1;
-- 删除多个一级分区
alter table t_b_add_drop_par_0108 drop partition p1,p2;
-- 删除一个二级分区
alter table t_b_add_drop_par_0108 drop subpartition p1_1;
-- 删除多个二级分区
alter table t_b_add_drop_par_0108 drop subpartition p1_1,p1_2;
-- 删除不存在的一级分区
alter table t_b_add_drop_par_0108 drop partition pnull;
-- 删除不存在的二级分区
alter table t_b_add_drop_par_0108 drop subpartition p_null;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0108') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0108')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0108;
drop tablespace ts_b_add_drop_par_0108;

