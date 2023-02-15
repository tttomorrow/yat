-- @testpoint: 验证原语法hash-hash分区表增删分区(主表指定非默认tablespace)，部分场景合理报错

drop tablespace if exists ts_b_add_drop_par_0111;
create tablespace ts_b_add_drop_par_0111 relative location 'ts_b_add_drop_par_0111';
drop table if exists t_b_add_drop_par_0111;
create table t_b_add_drop_par_0111(c1 int primary key,c2 int,c3 int)
tablespace ts_b_add_drop_par_0111
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
create index i_b_add_drop_par_0111_1 on t_b_add_drop_par_0111 (c1) global;
create index i_b_add_drop_par_0111_2 on t_b_add_drop_par_0111 (c2) local;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0111') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0111')) order by relname;

-- 非法添加一级二级分区报错
-- 添加一级分区不指定二级子分区
alter table t_b_add_drop_par_0111 add partition p3 values less than(300);
-- 添加一级分区指定一个二级分区
alter table t_b_add_drop_par_0111 add partition p4 values less than(400) (subpartition p4_1 values less than(400));
-- 添加一级分区指定多个二级分区
alter table t_b_add_drop_par_0111 add partition p5 values less than(500) (subpartition p5_1 values less than(450),subpartition p5_2 values less than(500));
-- 添加多个一级分区
alter table t_b_add_drop_par_0111 add partition p6 values less than(600) (subpartition p6_1 values less than(510)),add partition p7 values less than(700);
-- 为一级分区添加一个子分区
alter table t_b_add_drop_par_0111 modify partition p2 add subpartition p2_3 values less than(520);
-- 为一级分区添加多个子分区
alter table t_b_add_drop_par_0111 modify partition p2 add subpartition p2_3 values less than(530),modify partition p2 add subpartition p2_4 values less than(540);
-- 添加一级分区指定表空间
alter table t_b_add_drop_par_0111 add partition p8 values less than(800) tablespace ts_b_add_drop_par_0111;
-- 添加二级分区指定表空间
alter table t_b_add_drop_par_0111 modify partition p2 add subpartition p2_5 values less than(550) tablespace ts_b_add_drop_par_0111;
-- 分区重名
alter table t_b_add_drop_par_0111 add partition p2 values less than(900);
-- 一级分区值非法
alter table t_b_add_drop_par_0111 add partition p9 values less than(100);
-- 一级分区值合法，二级分区值非法
alter table t_b_add_drop_par_0111 add partition p9 values less than(900) (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50));
-- 一级分区值非法，二级分区值合法
alter table t_b_add_drop_par_0111 add partition p9 values less than(100) (subpartition p9_1 values less than(100),subpartition p9_2 values less than(200));
-- 一级分区值非法，二级分区值非法
alter table t_b_add_drop_par_0111 add partition p9 values less than(100) (subpartition p9_1 values less than(100),subpartition p9_2 values less than(50));
-- 一级分区数据类型非法
alter table t_b_add_drop_par_0111 add partition p9 values less than('a') (subpartition p9_1 values less than(100));
-- 二级分区值非法
alter table t_b_add_drop_par_0111 add partition p9 values less than(900) (subpartition p9_1 values less than('a'));
-- 一级分区指定表空间为pg_global
alter table t_b_add_drop_par_0111 add partition p8 values less than(900) tablespace pg_global;
-- 二级分区指定表空间为pg_global
alter table t_b_add_drop_par_0111 add partition p9 values less than(900) (subpartition p9_1 values less than(100) tablespace pg_global);

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0111') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0111')) order by relname;

-- 非法删除分区报错
-- 删除一个一级分区
alter table t_b_add_drop_par_0111 drop partition p1;
-- 删除多个一级分区
alter table t_b_add_drop_par_0111 drop partition p1,drop partition p2;
-- 删除一个二级分区
alter table t_b_add_drop_par_0111 drop subpartition p1_1;
-- 删除多个二级分区
alter table t_b_add_drop_par_0111 drop subpartition p1_1,drop subpartition p1_2;
-- 删除多个一级分区
alter table t_b_add_drop_par_0111 drop partition p1,drop partition p2;
-- 删除不存在的一级分区
alter table t_b_add_drop_par_0111 drop partition pnull;
-- 删除不存在的二级分区
alter table t_b_add_drop_par_0111 drop subpartition p_null;

select relname,boundaries,parttype from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0111') or parentid in (select oid from pg_partition where parentid in (select parentid from pg_partition where relname = 't_b_add_drop_par_0111')) order by relname;

-- 清理环境
drop table t_b_add_drop_par_0111;
drop tablespace ts_b_add_drop_par_0111;

