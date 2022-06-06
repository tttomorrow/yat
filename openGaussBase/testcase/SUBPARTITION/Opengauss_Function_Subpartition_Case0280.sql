-- @testpoint: range_range二级分区表：exchange/merge into/move/insert on duplicate key update,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0280;
drop tablespace if exists ts_subpartition_0280;
create tablespace ts_subpartition_0280 relative location 'subpartition_tablespace/subpartition_tablespace_0280';

--test1: alter table exchange
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0280
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
	check (col_4 is not null)
)tablespace ts_subpartition_0280
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step3: 创建普通表; expect:成功
drop table if exists t_subpartition_0280_01;
create   table if not exists t_subpartition_0280_01
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
	check (col_4 is not null)
)tablespace ts_subpartition_0280;
--step4: 普通表插入数据; expect:成功
insert into t_subpartition_0280_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 把普通表的数据迁移到二级分区表; expect:合理报错
alter table t_subpartition_0280 exchange partition (p_range_1) with table t_subpartition_0280_01 without validation;

--test2: alter table  merge into
--step6: 修改二级分区表，把多个一级分区合并为一个一级分区; expect:合理报错
alter table t_subpartition_0280 merge partitions p_range_1,p_range_2 into partition p_range_3;

--test3: alter table  move
--step7: 创建表空间; expect:成功
drop tablespace if exists ts_subpartition_0280_01;
create tablespace ts_subpartition_0280_01 relative location 'subpartition_tablespace/subpartition_tablespace_0280_01';
--step8: 修改二级分区表，移动一级分区到新的表空间; expect:合理报错
alter table t_subpartition_0280 move partition p_range_2 tablespace ts_subpartition_0280_01;

--test4: alter table  add partition
--step9: 修改二级分区表，添加一级分区; expect:成功
alter table t_subpartition_0280 add partition p_range_3 values less than( 30 );

--test5: insert --insert  on duplicate key update
--step10: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0280 cascade;
create   table if not exists t_subpartition_0280
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0280
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step11: 创建索引; expect:成功
create index on t_subpartition_0280(col_1,col_2) local;
--step12: 插入数据,指定on duplicate key update nothing; expect:成功
insert into t_subpartition_0280 values(1,11,1,1) on duplicate key update nothing;
--step13: 查询数据; expect:成功，有数据
select * from t_subpartition_0280 subpartition (p_range_1_2);

--step14: 插入不重复数据; expect:成功
insert into t_subpartition_0280 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step15: 插入重复数据; expect:成功
insert into t_subpartition_0280 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step16: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0280 subpartition (p_range_1_2);
--step17: 插入重复数据更新一级分区键; expect:成功
insert into t_subpartition_0280 values(1,11,1,1) on duplicate key update col_1=10;
--step18: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0280 values(1,11,1,1) on duplicate key update col_2=10;
--step19: 插入重复数据更新普通列; expect:成功
insert into t_subpartition_0280 values(1,11,1,1) on duplicate key update col_3=10;
--step20: 查询指定二级分区数据; expect:成功，数据更新
select * from t_subpartition_0280 subpartition (p_range_1_2);

--step21: 清理环境; expect:成功
drop table if exists t_subpartition_0280_01;
drop table if exists t_subpartition_0280 cascade;
drop tablespace if exists ts_subpartition_0280;
drop tablespace if exists ts_subpartition_0280_01;