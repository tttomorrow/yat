-- @testpoint: 验证原语法hash-list分区表增删分区，部分场景合理报错

drop tablespace if exists ts_b_add_drop_par_0097;
create tablespace ts_b_add_drop_par_0097 relative location 'ts_b_add_drop_par_0097';
drop table if exists t_b_add_drop_par_0097;
create table t_b_add_drop_par_0097(c1 int primary key,c2 int,c3 int)
partition by hash(c1) subpartition by list(c2) 
(
  partition p1
  (
    subpartition p1_1 values (1),
    subpartition p1_2 values (2)
  ),
  partition p2
  (
    subpartition p2_1 values (1),
    subpartition p2_2 values (2)
  ),
  partition p3
  (
    subpartition p3_1 values (1),
    subpartition p3_2 values (2)
  )
);
create index i_b_add_drop_par_0097_1 on t_b_add_drop_par_0097 (c1) global;
create index i_b_add_drop_par_0097_2 on t_b_add_drop_par_0097 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0097') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0097')) order by relname;

-- 合法添加一级、二级分区成功
-- 为一级分区添加一个子分区
alter table t_b_add_drop_par_0097 modify partition p1 add subpartition p1_3 values (3);
-- 为一级分区添加多个子分区
alter table t_b_add_drop_par_0097 modify partition p1 add subpartition p1_4 values (4),modify partition p1 add subpartition p1_5 values (5);
-- 添加二级分区指定表空间
alter table t_b_add_drop_par_0097 modify partition p1 add subpartition p1_6 values (6) tablespace ts_b_add_drop_par_0097;

-- 非法添加一级二级分区报错
-- 添加一级分区不指定二级子分区
alter table t_b_add_drop_par_0097 add partition p4;
alter table t_b_add_drop_par_0097 add partition p4 values less than(300);
-- 添加一级分区指定一个二级分区
alter table t_b_add_drop_par_0097 add partition p4 (subpartition p4_1 values (4));
alter table t_b_add_drop_par_0097 add partition p4 values less than(400) (subpartition p4_1 values (4));
-- 添加一级分区指定多个二级分区
alter table t_b_add_drop_par_0097 add partition p4 (subpartition p4_1 values (4),subpartition p4_2 values (5));
alter table t_b_add_drop_par_0097 add partition p4 values less than(500) (subpartition p4_1 values (4),subpartition p4_2 values (5));
-- 添加多个一级分区
alter table t_b_add_drop_par_0097 add partition p4 (subpartition p4_1 values (5)),add partition p5 values (1);
alter table t_b_add_drop_par_0097 add partition p4 values less than(600) (subpartition p4_1 values (5)),add partition p5 values (1);
-- 添加一级分区指定表空间
alter table t_b_add_drop_par_0097 add partition p4 tablespace ts_b_add_drop_par_0097;
alter table t_b_add_drop_par_0097 add partition p4 values less than(800) tablespace ts_b_add_drop_par_0097;
-- 分区重名
alter table t_b_add_drop_par_0097 add partition p1;
alter table t_b_add_drop_par_0097 add partition p1 values less than(900);
-- 二级分区值非法
alter table t_b_add_drop_par_0097 add partition p9 values (subpartition p9_1 values (1),subpartition p9_2 values (1));
alter table t_b_add_drop_par_0097 add partition p9 values less than(900) (subpartition p9_1 values (1),subpartition p9_2 values (1));
-- 一级分区数据类型非法
alter table t_b_add_drop_par_0097 add partition p9 values less than('a') (subpartition p9_1 values (1));
-- 二级分区值非法
alter table t_b_add_drop_par_0097 add partition p9 (subpartition p9_1 values ('a'));
alter table t_b_add_drop_par_0097 add partition p9 values less than(900) (subpartition p9_1 values ('a'));
-- 一级分区指定表空间为pg_global
alter table t_b_add_drop_par_0097 add partition p8 tablespace pg_global;
alter table t_b_add_drop_par_0097 add partition p8 values less than(900) tablespace pg_global;
-- 二级分区指定表空间为pg_global
alter table t_b_add_drop_par_0097 add partition p9 (subpartition p9_1 values (100) tablespace pg_global);
alter table t_b_add_drop_par_0097 add partition p9 values less than(900) (subpartition p9_1 values (1) tablespace pg_global);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0097') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0097')) order by relname;

-- 合法删除分区成功
-- 删除一个二级分区
alter table t_b_add_drop_par_0097 drop subpartition p2_1;
-- 删除多个二级分区
alter table t_b_add_drop_par_0097 drop subpartition p1_1,drop subpartition p1_2,drop subpartition p1_3,drop subpartition p1_4,drop subpartition p1_5;

-- 非法删除分区报错
-- 删除一个一级分区
alter table t_b_add_drop_par_0097 drop partition p2;
-- 删除多个一级分区
alter table t_b_add_drop_par_0097 drop partition p1,drop partition p2;
-- 删除一级分区的最后一个二级分区
alter table t_b_add_drop_par_0097 drop subpartition p1_6;
-- 删除不存在的一级分区
alter table t_b_add_drop_par_0097 drop partition pnull;
-- 删除不存在的二级分区
alter table t_b_add_drop_par_0097 drop subpartition p_null;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0097') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0097')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0097;
drop tablespace ts_b_add_drop_par_0097;

