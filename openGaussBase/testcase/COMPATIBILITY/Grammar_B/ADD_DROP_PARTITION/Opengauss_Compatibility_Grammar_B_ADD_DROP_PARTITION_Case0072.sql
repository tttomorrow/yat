-- @testpoint: 验证MySQL兼容语法list-range分区表增删分区(主表指定非默认tablespace)，部分场景合理报错

drop tablespace if exists ts_b_add_drop_par_0072;
create tablespace ts_b_add_drop_par_0072 relative location 'ts_b_add_drop_par_0072';
drop table if exists t_b_add_drop_par_0072;
create table t_b_add_drop_par_0072(c1 char(1),c2 int,c3 int primary key)
tablespace ts_b_add_drop_par_0072
partition by list(c1) subpartition by range(c2) 
(
  partition p1 values ('a')
  (
    subpartition p1_1 values less than (100),
    subpartition p1_2 values less than (200)
  ),
  partition p2 values ('b')
  (
    subpartition p2_1 values less than (100),
    subpartition p2_2 values less than (200)
  )
);
create index i_b_add_drop_par_0072_1 on t_b_add_drop_par_0072 (c1) global;
create index i_b_add_drop_par_0072_2 on t_b_add_drop_par_0072 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0072') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0072')) order by relname;

-- 合法添加一级、二级分区成功
-- 添加一级分区不指定二级子分区
alter table t_b_add_drop_par_0072 add partition (partition p3 values ('c'));
-- 添加一级分区指定一个二级分区
alter table t_b_add_drop_par_0072 add partition (partition p4 values ('d') (subpartition p4_1 values less than(100)));
-- 添加一级分区指定多个二级分区
alter table t_b_add_drop_par_0072 add partition (partition p5 values ('e') (subpartition p5_1 values less than(100),subpartition p5_2 values less than(200)));
-- 添加多个一级分区
alter table t_b_add_drop_par_0072 add partition (partition p6 values ('f') (subpartition p6_1 values less than(100)),partition p7 values ('g'));
-- 为一级分区添加一个子分区
alter table t_b_add_drop_par_0072 modify partition p6 add subpartition p6_2 values less than(200);
-- 为一级分区添加多个子分区
alter table t_b_add_drop_par_0072 modify partition p6 add subpartition p6_3 values less than(300),modify partition p6 add subpartition p6_4 values less than(400);
-- 添加一级分区指定表空间
alter table t_b_add_drop_par_0072 add partition (partition p8 values ('h') tablespace ts_b_add_drop_par_0072);
-- 添加二级分区指定表空间
alter table t_b_add_drop_par_0072 modify partition p6 add subpartition p6_5 values less than(500) tablespace ts_b_add_drop_par_0072;

-- 非法添加一级二级分区报错
-- 分区重名
alter table t_b_add_drop_par_0072 add partition (partition p8 values ('z'));
-- 一级分区值非法
alter table t_b_add_drop_par_0072 add partition (partition p9 values ('a'));
-- 一级分区值合法，二级分区值非法
alter table t_b_add_drop_par_0072 add partition (partition p9 values ('k') (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50)));
-- 一级分区值非法，二级分区值合法
alter table t_b_add_drop_par_0072 add partition (partition p9 values ('a') (subpartition p9_1 values less than(100),subpartition p9_2 values less than(200)));
-- 一级分区值非法，二级分区值非法
alter table t_b_add_drop_par_0072 add partition (partition p9 values ('a') (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50)));
-- 一级分区数据类型非法
alter table t_b_add_drop_par_0072 add partition (partition p9 values ('aa') (subpartition p9_1 values less than(100)));
-- 二级分区值非法
alter table t_b_add_drop_par_0072 add partition (partition p9 values ('k') (subpartition p9_1 values less than('a')));
-- 一级分区指定表空间为pg_global
alter table t_b_add_drop_par_0072 add partition (partition p8 values ('k') tablespace pg_global);
-- 二级分区指定表空间为pg_global
alter table t_b_add_drop_par_0072 add partition (partition p9 values ('k') (subpartition p9_1 values less than(100) tablespace pg_global));

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0072') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0072')) order by relname;

-- 合法删除分区成功
-- 删除一个一级分区
alter table t_b_add_drop_par_0072 drop partition p8;
-- 删除多个一级分区
alter table t_b_add_drop_par_0072 drop partition p1,p2;
-- 删除一个二级分区
alter table t_b_add_drop_par_0072 drop subpartition p6_1;
-- 删除多个二级分区
alter table t_b_add_drop_par_0072 drop subpartition p6_2,p6_3,p6_4;
-- 删除多个一级分区
alter table t_b_add_drop_par_0072 drop partition p3,p4,p5,p7;

-- 非法删除分区报错
-- 删除一级分区的最后一个二级分区
alter table t_b_add_drop_par_0072 drop subpartition p6_5;
-- 删除表的最后一个一级分区
alter table t_b_add_drop_par_0072 drop partition p6;
-- 删除不存在的一级分区
alter table t_b_add_drop_par_0072 drop partition pnull;
-- 删除不存在的二级分区
alter table t_b_add_drop_par_0072 drop subpartition p_null;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0072') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0072')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0072;
drop tablespace ts_b_add_drop_par_0072;

