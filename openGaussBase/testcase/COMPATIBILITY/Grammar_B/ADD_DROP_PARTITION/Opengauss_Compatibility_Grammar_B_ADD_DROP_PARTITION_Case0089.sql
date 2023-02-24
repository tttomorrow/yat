-- @testpoint: 验证原语法hash-range分区表增删分区，部分场景合理报错

drop tablespace if exists ts_b_add_drop_par_0089;
create tablespace ts_b_add_drop_par_0089 relative location 'ts_b_add_drop_par_0089';
drop table if exists t_b_add_drop_par_0089;
create table t_b_add_drop_par_0089(c1 int primary key,c2 int,c3 int)
partition by hash(c1) subpartition by range(c2) 
(
  partition p1
  (
    subpartition p1_1 values less than (100),
    subpartition p1_2 values less than (200)
  ),
  partition p2
  (
    subpartition p2_1 values less than (100),
    subpartition p2_2 values less than (200)
  ),
  partition p3
  (
    subpartition p3_1 values less than (100),
    subpartition p3_2 values less than (200)
  )
);
create index i_b_add_drop_par_0089_1 on t_b_add_drop_par_0089 (c1) global;
create index i_b_add_drop_par_0089_2 on t_b_add_drop_par_0089 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0089') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0089')) order by relname;

-- 合法添加一级、二级分区成功
-- 为一级分区添加一个子分区
alter table t_b_add_drop_par_0089 modify partition p1 add subpartition p1_3 values less than(300);
-- 为一级分区添加多个子分区
alter table t_b_add_drop_par_0089 modify partition p1 add subpartition p1_4 values less than(400),modify partition p1 add subpartition p1_5 values less than(500);
-- 添加二级分区指定表空间
alter table t_b_add_drop_par_0089 modify partition p1 add subpartition p1_6 values less than(600) tablespace ts_b_add_drop_par_0089;

-- 非法添加一级二级分区报错
-- 添加一级分区不指定二级子分区
alter table t_b_add_drop_par_0089 add partition p4;
alter table t_b_add_drop_par_0089 add partition p4 values less than(300);
-- 添加一级分区指定一个二级分区
alter table t_b_add_drop_par_0089 add partition p4 (subpartition p4_1 values less than(400));
alter table t_b_add_drop_par_0089 add partition p4 values less than(400) (subpartition p4_1 values less than(400));
-- 添加一级分区指定多个二级分区
alter table t_b_add_drop_par_0089 add partition p4 (subpartition p4_1 values less than(450),subpartition p4_2 values less than(500));
alter table t_b_add_drop_par_0089 add partition p4 values less than(500) (subpartition p4_1 values less than(450),subpartition p4_2 values less than(500));
-- 添加多个一级分区
alter table t_b_add_drop_par_0089 add partition p4 (subpartition p4_1 values less than(510)),add partition p5 values less than(100);
alter table t_b_add_drop_par_0089 add partition p4 values less than(600) (subpartition p4_1 values less than(510)),add partition p5 values less than(100);
-- 添加一级分区指定表空间
alter table t_b_add_drop_par_0089 add partition p4 tablespace ts_b_add_drop_par_0089;
alter table t_b_add_drop_par_0089 add partition p4 values less than(800) tablespace ts_b_add_drop_par_0089;
-- 分区重名
alter table t_b_add_drop_par_0089 add partition p1;
alter table t_b_add_drop_par_0089 add partition p1 values less than(900);
-- 二级分区值非法
alter table t_b_add_drop_par_0089 add partition p9 values (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50));
alter table t_b_add_drop_par_0089 add partition p9 values less than(900) (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50));
-- 一级分区数据类型非法
alter table t_b_add_drop_par_0089 add partition p9 values less than('a') (subpartition p9_1 values less than(100));
-- 二级分区值非法
alter table t_b_add_drop_par_0089 add partition p9 (subpartition p9_1 values less than('a'));
alter table t_b_add_drop_par_0089 add partition p9 values less than(900) (subpartition p9_1 values less than('a'));
-- 一级分区指定表空间为pg_global
alter table t_b_add_drop_par_0089 add partition p8 tablespace pg_global;
alter table t_b_add_drop_par_0089 add partition p8 values less than(900) tablespace pg_global;
-- 二级分区指定表空间为pg_global
alter table t_b_add_drop_par_0089 add partition p9 (subpartition p9_1 values less than(100) tablespace pg_global);
alter table t_b_add_drop_par_0089 add partition p9 values less than(900) (subpartition p9_1 values less than(100) tablespace pg_global);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0089') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0089')) order by relname;

-- 合法删除分区成功
-- 删除一个二级分区
alter table t_b_add_drop_par_0089 drop subpartition p2_1;
-- 删除多个二级分区
alter table t_b_add_drop_par_0089 drop subpartition p1_1,drop subpartition p1_2,drop subpartition p1_3,drop subpartition p1_4,drop subpartition p1_5;

-- 非法删除分区报错
-- 删除一个一级分区
alter table t_b_add_drop_par_0089 drop partition p2;
-- 删除多个一级分区
alter table t_b_add_drop_par_0089 drop partition p1,drop partition p2;
-- 删除一级分区的最后一个二级分区
alter table t_b_add_drop_par_0089 drop subpartition p1_6;
-- 删除不存在的一级分区
alter table t_b_add_drop_par_0089 drop partition pnull;
-- 删除不存在的二级分区
alter table t_b_add_drop_par_0089 drop subpartition p_null;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0089') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0089')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0089;
drop tablespace ts_b_add_drop_par_0089;

