-- @testpoint: list_list二级分区表：同义词/主键外键/pg_constraint,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0068;
drop tablespace if exists ts_subpartition_0068;
create tablespace ts_subpartition_0068 relative location 'subpartition_tablespace/subpartition_tablespace_0068';
--test1: 同义词
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0068
(
    col_1 int,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0068
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
    subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
    subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step3:  创建表同义词; expect:成功
drop synonym if exists partition_t;
create or replace synonym partition_t for t_subpartition_0068;
--step4:  查询表同义词数据; expect:成功
select * from partition_t;

--test2: 使用同义词对数据操作
--step5: 插入数据; expect:成功
insert into partition_t values(0,0,0,0);
insert into partition_t values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into partition_t values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into partition_t values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
insert into  partition_t values (generate_series(-19, 19),generate_series(-10, 100),generate_series(0, 99));
update partition_t set col_2=8 where col_2=4;
delete partition_t where col_2=8;
select count(*) from partition_t;

--step6: 创建视图; expect:成功
drop view if exists t_subpartition_0068_view;
create view t_subpartition_0068_view as select * from t_subpartition_0068;
--step7: 对视图创建同义词; expect:成功
drop synonym if exists partition_tv;
create synonym partition_tv for t_subpartition_0068_view;
--step8: 查看视图同义词数据; expect:成功
select count(*) from partition_tv;
--step9: 删除视图同义词数据; expect:合理报错
delete partition_tv where col_2=8;
--step10: 删除同义词; expect:合理报错
drop synonym if exists partition_tv;
drop synonym if exists partition_t;

--test3: 主键外键
--step11: 创建普通表，指定主键; expect:成功
drop table if exists t_subpartition_0068_01 cascade;
create table t_subpartition_0068_01
(
    col_1 int primary key,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
);
--step12: 创建二级分区表,指定外键; expect:成功
drop table if exists t_subpartition_0068 cascade;
create table t_subpartition_0068
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int ,
    foreign key(col_1) references t_subpartition_0068_01(col_1)
)
tablespace ts_subpartition_0068
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
    subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
    subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step13: 向二级分区表插入普通表没有的数据; expect:合理报错
insert into t_subpartition_0068 values(0,0,0,0);
--step14: 插入数据; expect:成功
insert into t_subpartition_0068_01 values(0,0,0,0);
insert into t_subpartition_0068 values(0,0,0,0);
--step15: 更新数据; expect:成功
update t_subpartition_0068 set col_2=8 where col_2=0;
--step16: 更新二级分区表数据为普通表没有的数据; expect:合理报错
update t_subpartition_0068 set col_1=8 where col_2=8;
--step17: 删除数据; expect:成功
delete t_subpartition_0068 where col_2=8;
--step18: 更新普通表数据; expect:成功
update t_subpartition_0068_01 set col_1=8 where col_2=0;

--test4: pg_constraint
--step19: 清空普通表数据; expect:合理报错
truncate t_subpartition_0068_01;
--step20: 指定cascade清空普通表数据; expect:成功
truncate t_subpartition_0068_01 cascade;
--step21: 查询pg_constraint数据; expect:成功
select conname,contype,condeferrable,condeferred,convalidated from pg_constraint where conname='t_subpartition_0068_col_1_fkey';

--step22: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0068_01 cascade;
drop table if exists t_subpartition_0068;
drop tablespace if exists ts_subpartition_0068;