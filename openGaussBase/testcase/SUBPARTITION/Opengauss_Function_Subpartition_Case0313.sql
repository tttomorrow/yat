-- @testpoint: range_hash二级分区表：表约束(约束推迟)/null/not null,部分测试点合理报错

--test1: 表约束：not null约束推迟
--step1: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0313;
create table if not exists t_subpartition_0313
(
    col_1 int ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int ,
    primary key (col_1,col_2) deferrable
)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step2: 开始一个事务; expect:成功
start transaction;
--step3: 设置所有约束在事务提交时检查; expect:成功
set constraints all deferred;
--step4: 插入符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0313 values(111,111,111),(118,118,118),(205,205,205),(505,505,505);
--step5: 插入不符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0313 values(111,111,111),(118,118,118),(205,205,205),(505,505,505);
--step6: 提交事务; expect:合理报错
commit;
--step7: 结束事务; expect:成功
end;

--test2: 列约束not null
--step8: 创建二级分区表,二级分区键包含列约束not null; expect:成功
drop table if exists t_subpartition_00313;
create table if not exists t_subpartition_0313
(
    col_1 int ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int   
)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step9: 非空约束列插入空数据; expect:合理报错
insert into t_subpartition_0313(col_1,col_2) values(1,1),(5,5);
--test3: 列约束null
--step10: 创建二级分区表,二级分区键包含列约束null; expect:成功
drop table if exists t_subpartition_00313;
create table if not exists t_subpartition_0313
(
    col_1 int ,
    col_2 int  null ,
    col_3 int ,
    col_4 int   
)
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step11: 空约束列插入空数据; expect:合理报错
insert into t_subpartition_0313(col_1,col_3,col_4) values(1,1,1),(5,5,5);

--step12: 清理环境; expect:成功
drop table if exists t_subpartition_0313;