-- @testpoint: range_list二级分区表：同义词/主键外键/pg_constraint,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0240;
drop tablespace if exists ts_subpartition_0240;
create tablespace ts_subpartition_0240 relative location 'subpartition_tablespace/subpartition_tablespace_0240';
--test1: 同义词
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0240
(
    col_1 int,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0240
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 创建表同义词; expect:成功
drop synonym if exists partition_t;
create or replace synonym partition_t for t_subpartition_0240;
--step4: 查询表同义词数据; expect:成功
select * from partition_t;
--step5: 创建普通表并插入数据; expect:成功
drop table if exists t_subpartition_0240_01;
create table if not exists t_subpartition_0240_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0240;
insert into t_subpartition_0240_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);

--test2: 使用同义词对数据操作
--step6: 增删改查操作; expect:成功
insert into partition_t values(0,0,0,0);
insert into partition_t values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into partition_t values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into partition_t values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
insert into  partition_t values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
insert into partition_t(col_1,col_2,col_3) select col_1,to_char(col_2),col_2 from t_subpartition_0240_01 where col_1>5;
update partition_t set col_2=8 where col_2=4;
update t_subpartition_0240 set col_1=10 where col_3>8 and col_2 between 9 and 199;
update partition_t set col_1=10 where col_3>8 and col_2 between 9 and 199;
delete partition_t where col_2=8;
select count(*) from partition_t;

--step7: 创建视图; expect:成功
drop view if exists t_subpartition_0240_view;
create view t_subpartition_0240_view as select * from t_subpartition_0240;
--step8: 对视图创建同义词; expect:成功
drop synonym if exists partition_tv;
create synonym partition_tv for t_subpartition_0240_view;
--step9: 查看视图同义词数据; expect:成功
select count(*) from partition_tv;
--step10: 删除同义词; expect:成功
drop synonym partition_tv;
drop synonym partition_t;

--test3: 主键外键
--step11: 创建普通表,指定主键; expect:成功
drop table if exists t_subpartition_0240_01 cascade;
create table t_subpartition_0240_01
(
    col_1 int primary key,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
);
--step12: 创建二级分区表,指定外键; expect:成功
drop table if exists t_subpartition_0240 cascade;
create table t_subpartition_0240
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int ,
    foreign key(col_1) references t_subpartition_0240_01(col_1)
)
tablespace ts_subpartition_0240
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step13: 向二级分区表插入普通表没有的数据; expect:合理报错
insert into t_subpartition_0240 values(0,0,0,0);
--step14: 插入数据; expect:成功
insert into t_subpartition_0240_01 values(0,0,0,0);
insert into t_subpartition_0240 values(0,0,0,0);
--step15: 更新数据; expect:成功
update t_subpartition_0240 set col_2=8 where col_2=0;
--step16: 更新二级分区表数据为普通表没有的数据; expect:合理报错
update t_subpartition_0240 set col_1=8 where col_2=8;
--step17: 删除数据; expect:成功
delete t_subpartition_0240 where col_2=8;
--step18: 更新普通表数据; expect:成功
update t_subpartition_0240_01 set col_1=8 where col_2=0;

--test4: pg_constraint
--step19: 清空普通表数据; expect:合理报错
truncate t_subpartition_0240_01;
--step20: 指定cascade清空普通表数据; expect:成功
truncate t_subpartition_0240_01 cascade;
--step21: 查询pg_constraint数据; expect:成功
select conname,contype,condeferrable,condeferred,convalidated from pg_constraint where conname='t_subpartition_0240_col_1_fkey';

--step22: 清理环境; expect:成功
drop table if exists t_subpartition_0240_01  cascade;
drop table if exists t_subpartition_0240  cascade;
drop tablespace if exists ts_subpartition_0240;