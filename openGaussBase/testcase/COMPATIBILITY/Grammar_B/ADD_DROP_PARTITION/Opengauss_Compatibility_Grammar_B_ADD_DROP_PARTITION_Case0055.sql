-- @testpoint: 验证原语法range-list分区表增删分区(主表指定非默认tablespace)，部分场景合理报错

drop tablespace if exists ts_b_add_drop_par_0055;
create tablespace ts_b_add_drop_par_0055 relative location 'ts_b_add_drop_par_0055';
drop table if exists t_b_add_drop_par_0055;
create table t_b_add_drop_par_0055(c1 int primary key,c2 char(1),c3 int)
tablespace ts_b_add_drop_par_0055
partition by range(c1) subpartition by list(c2) 
(
  partition p1 values less than (100)
  (
    subpartition p1_1 values ('a'),
    subpartition p1_2 values ('b')
  ),
  partition p2 values less than (200)
  (
    subpartition p2_1 values ('c'),
    subpartition p2_2 values ('d')
  )
);
create index i_b_add_drop_par_0055_1 on t_b_add_drop_par_0055 (c1) global;
create index i_b_add_drop_par_0055_2 on t_b_add_drop_par_0055 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0055') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0055')) order by relname;

-- 合法添加一级、二级分区成功
-- 添加一级分区不指定二级子分区
alter table t_b_add_drop_par_0055 add partition p3 values less than(300);
-- 添加一级分区指定一个二级分区
alter table t_b_add_drop_par_0055 add partition p4 values less than(400) (subpartition p4_1 values ('e'));
-- 添加一级分区指定多个二级分区
alter table t_b_add_drop_par_0055 add partition p5 values less than(500) (subpartition p5_1 values ('f'),subpartition p5_2 values ('g'));
-- 添加多个一级分区
alter table t_b_add_drop_par_0055 add partition p6 values less than(600) (subpartition p6_1 values ('h')),add partition p7 values less than(700);
-- 为一级分区添加一个子分区
alter table t_b_add_drop_par_0055 modify partition p6 add subpartition p6_2 values ('i');
-- 为一级分区添加多个子分区
alter table t_b_add_drop_par_0055 modify partition p6 add subpartition p6_3 values ('j'),modify partition p6 add subpartition p6_4 values ('k');
-- 添加一级分区指定表空间
alter table t_b_add_drop_par_0055 add partition p8 values less than(800) tablespace ts_b_add_drop_par_0055;
-- 添加二级分区指定表空间
alter table t_b_add_drop_par_0055 modify partition p6 add subpartition p6_5 values ('l') tablespace ts_b_add_drop_par_0055;

-- 非法添加一级二级分区报错
-- 分区重名
alter table t_b_add_drop_par_0055 add partition p8 values less than(900);
-- 一级分区值非法
alter table t_b_add_drop_par_0055 add partition p9 values less than(100);
-- 一级分区值合法，二级分区值非法
alter table t_b_add_drop_par_0055 add partition p9 values less than(900) (subpartition p9_1 values ('m'),subpartition p9_2 values ('m'));
-- 一级分区值非法，二级分区值合法
alter table t_b_add_drop_par_0055 add partition p9 values less than(100) (subpartition p9_1 values ('m'),subpartition p9_2 values ('n'));
-- 一级分区值非法，二级分区值非法
alter table t_b_add_drop_par_0055 add partition p9 values less than(100) (subpartition p9_1 values ('m'),subpartition p9_2 values ('m'));
-- 一级分区数据类型非法
alter table t_b_add_drop_par_0055 add partition p9 values less than('a') (subpartition p9_1 values ('m'));
-- 二级分区值非法
alter table t_b_add_drop_par_0055 add partition p9 values less than(900) (subpartition p9_1 values ('aa'));
-- 一级分区指定表空间为pg_global
alter table t_b_add_drop_par_0055 add partition p8 values less than(900) tablespace pg_global;
-- 二级分区指定表空间为pg_global
alter table t_b_add_drop_par_0055 add partition p9 values less than(900) (subpartition p9_1 values ('m') tablespace pg_global);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0055') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0055')) order by relname;

-- 合法删除分区成功
-- 删除一个一级分区
alter table t_b_add_drop_par_0055 drop partition p8;
-- 删除多个一级分区
alter table t_b_add_drop_par_0055 drop partition p1,drop partition p2;
-- 删除一个二级分区
alter table t_b_add_drop_par_0055 drop subpartition p6_1;
-- 删除多个二级分区
alter table t_b_add_drop_par_0055 drop subpartition p6_2,drop subpartition p6_3,drop subpartition p6_4;
-- 删除多个一级分区
alter table t_b_add_drop_par_0055 drop partition p3,drop partition p4,drop partition p5,drop partition p7;

-- 非法删除分区报错
-- 删除一级分区的最后一个二级分区
alter table t_b_add_drop_par_0055 drop subpartition p6_5;
-- 删除表的最后一个一级分区
alter table t_b_add_drop_par_0055 drop partition p6;
-- 删除不存在的一级分区
alter table t_b_add_drop_par_0055 drop partition pnull;
-- 删除不存在的二级分区
alter table t_b_add_drop_par_0055 drop subpartition p_null;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0055') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0055')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0055;
drop tablespace ts_b_add_drop_par_0055;

