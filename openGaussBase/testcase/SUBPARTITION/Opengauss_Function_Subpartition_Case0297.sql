-- @testpoint: range_range二级分区表：同义词/主键外键/pg_constraint,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0297;
drop tablespace if exists ts_subpartition_0297;
create tablespace ts_subpartition_0297 relative location 'subpartition_tablespace/subpartition_tablespace_0297';
--test1: 同义词
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0297
(
    col_1 int,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0297
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
);
--step3: 创建表同义词; expect:成功
drop synonym if exists partition_t;
create or replace synonym partition_t for t_subpartition_0297;
--step4: 查询表同义词数据; expect:成功
select * from partition_t;

--test2: 使用同义词对数据操作
--step5: 插入数据; expect:成功
insert into partition_t values(0,0,0,0);
insert into partition_t values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into partition_t values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into partition_t values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
insert into  partition_t values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
update partition_t set col_2=8 where col_2=4;
delete partition_t where col_2=8;
select count(*) from partition_t;
--step6: 创建视图; expect:成功
drop view if exists t_subpartition_0297_view;
create view t_subpartition_0297_view as select * from t_subpartition_0297;
--step7: 对视图创建同义词; expect:成功
drop synonym if exists partition_tv;
create synonym partition_tv for t_subpartition_0297_view;
--step8: 查看视图同义词数据; expect:成功
select count(*) from partition_tv;
--step9: 删除同义词; expect:成功
drop synonym partition_tv;
drop synonym partition_t;

--test3: 主键外键
--step10: 创建普通表,指定主键; expect:成功
drop table if exists t_subpartition_0297_01 cascade;
create table t_subpartition_0297_01
(
    col_1 int primary key,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
);
--step11: 创建二级分区表,指定外键; expect:成功
drop table if exists t_subpartition_0297 cascade;
create table t_subpartition_0297
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int ,
    foreign key(col_1) references t_subpartition_0297_01(col_1)  deferrable
)
tablespace ts_subpartition_0297
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
);
--step12: 向二级分区表插入普通表没有的数据; expect:合理报错
insert into t_subpartition_0297 values(0,0,0,0); 
--step13: 插入数据; expect:成功
insert into t_subpartition_0297_01 values(0,0,0,0);
insert into t_subpartition_0297 values(0,0,0,0);
--step14: 更新数据; expect:成功
update t_subpartition_0297 set col_2=8 where col_2=0;
--step15: 更新二级分区表数据为普通表没有的数据; expect:合理报错
update t_subpartition_0297 set col_1=8 where col_2=8;
--step16: 删除数据; expect:成功
delete t_subpartition_0297 where col_2=8;
--step17: 更新普通表数据; expect:成功
update t_subpartition_0297_01 set col_1=8 where col_2=0;

--test4: pg_constraint
--step18: 清空普通表数据; expect:合理报错
truncate t_subpartition_0297_01;
--step19: 指定cascade清空普通表数据; expect:成功
truncate t_subpartition_0297_01 cascade;
--step20: 查询pg_constraint数据; expect:成功
select conname,contype,condeferrable,condeferred,convalidated from pg_constraint where conname='t_subpartition_0297_col_1_fkey';

--step21: 清理环境; expect:成功
drop table if exists t_subpartition_0297_01  cascade;
drop table if exists t_subpartition_0297  cascade;
drop tablespace if exists ts_subpartition_0297;