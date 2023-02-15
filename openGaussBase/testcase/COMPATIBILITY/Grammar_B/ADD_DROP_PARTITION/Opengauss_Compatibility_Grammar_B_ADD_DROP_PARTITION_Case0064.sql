-- @testpoint: 验证MySQL兼容语法range-hash分区表增删分区(主表指定非默认tablespace)，部分场景合理报错

drop tablespace if exists ts_b_add_drop_par_0064;
create tablespace ts_b_add_drop_par_0064 relative location 'ts_b_add_drop_par_0064';
drop table if exists t_b_add_drop_par_0064;
create table t_b_add_drop_par_0064(c1 int primary key,c2 int,c3 int)
tablespace ts_b_add_drop_par_0064
partition by range(c1) subpartition by hash(c2) 
(
  partition p1 values less than (100)
  (
    subpartition p1_1,
    subpartition p1_2
  ),
  partition p2 values less than (200)
  (
    subpartition p2_1,
    subpartition p2_2
  )
);
create index i_b_add_drop_par_0064_1 on t_b_add_drop_par_0064 (c1) global;
create index i_b_add_drop_par_0064_2 on t_b_add_drop_par_0064 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0064') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0064')) order by relname;

-- 合法添加一级、二级分区成功
-- 添加一级分区不指定二级子分区
alter table t_b_add_drop_par_0064 add partition (partition p3 values less than(300));
-- 添加一级分区指定一个二级分区
alter table t_b_add_drop_par_0064 add partition (partition p4 values less than(400) (subpartition p4_1));
-- 添加一级分区指定多个二级分区
alter table t_b_add_drop_par_0064 add partition (partition p5 values less than(500) (subpartition p5_1,subpartition p5_2,subpartition p5_3,subpartition p5_4,subpartition p5_5));
-- 添加多个一级分区
alter table t_b_add_drop_par_0064 add partition (partition p6 values less than(600) (subpartition p6_1),partition p7 values less than(700));
-- 添加一级分区指定表空间
alter table t_b_add_drop_par_0064 add partition (partition p8 values less than(800) tablespace ts_b_add_drop_par_0064);

-- 非法添加一级二级分区报错
-- 为一级分区添加一个hash子分区
alter table t_b_add_drop_par_0064 modify partition p6 add subpartition p6_2;
alter table t_b_add_drop_par_0064 modify partition p6 add subpartition p6_2 values(1);
-- 为一级分区添加多个hash子分区
alter table t_b_add_drop_par_0064 modify partition p6 add subpartition p6_3,modify partition p6 add subpartition p6_4;
alter table t_b_add_drop_par_0064 modify partition p6 add subpartition p6_3 values(1),modify partition p6 add subpartition p6_4 values(1);
-- 添加二级hash分区指定表空间
alter table t_b_add_drop_par_0064 modify partition p6 add subpartition p6_5 tablespace ts_b_add_drop_par_0064;
alter table t_b_add_drop_par_0064 modify partition p6 add subpartition p6_5 values ('l') tablespace ts_b_add_drop_par_0064;
-- 分区重名
alter table t_b_add_drop_par_0064 add partition (partition p8 values less than(900));
-- 一级分区值非法
alter table t_b_add_drop_par_0064 add partition (partition p9 values less than(100));
-- 一级分区数据类型非法
alter table t_b_add_drop_par_0064 add partition (partition p9 values less than('a') (subpartition p9_1));
-- 二级分区值非法
alter table t_b_add_drop_par_0064 add partition (partition p9 values less than(900) (subpartition p9_1 values ('a')));
-- 一级分区指定表空间为pg_global
alter table t_b_add_drop_par_0064 add partition (partition p8 values less than(900) tablespace pg_global);
-- 二级分区指定表空间为pg_global
alter table t_b_add_drop_par_0064 add partition (partition p9 values less than(900) (subpartition p9_1 tablespace pg_global));

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0064') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0064')) order by relname;

-- 合法删除分区成功
-- 删除一个一级分区
alter table t_b_add_drop_par_0064 drop partition p8;
-- 删除多个一级分区
alter table t_b_add_drop_par_0064 drop partition p1,p2;
-- 删除多个一级分区
alter table t_b_add_drop_par_0064 drop partition p3,p4,p6,p7;

-- 非法删除分区报错
-- 删除一个二级分区
alter table t_b_add_drop_par_0064 drop subpartition p5_1;
-- 删除多个二级分区
alter table t_b_add_drop_par_0064 drop subpartition p5_2,p5_3,p5_4;
-- 删除表的最后一个一级分区
alter table t_b_add_drop_par_0064 drop partition p5;
-- 删除不存在的一级分区
alter table t_b_add_drop_par_0064 drop partition pnull;
-- 删除不存在的二级分区
alter table t_b_add_drop_par_0064 drop subpartition p_null;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0064') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0064')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0064;
drop tablespace ts_b_add_drop_par_0064;

