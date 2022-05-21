-- @testpoint: range_hash二级分区表：truncate/delete,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0334;
drop tablespace if exists ts_subpartition_0334;
create tablespace ts_subpartition_0334 relative location 'subpartition_tablespace/subpartition_tablespace_0334';

--test1: truncate  table
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0334
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0334
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
    subpartition t_subpartition_0334
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0334 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step4: 查询数据; expect:成功,有数据
select * from t_subpartition_0334;
--step5: 清空表数据; expect:成功
truncate t_subpartition_0334;
--step6: 查询数据; expect:成功,无数据
select * from t_subpartition_0334;

--test2: truncate  partition
--step7: 插入数据; expect:成功
insert into t_subpartition_0334 values(-11,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 查询指定一级分区数据; expect:成功,有数据
select * from t_subpartition_0334 partition(p_range_1);
--step9: 查询指定一级分区数据; expect:成功,有数据
select * from t_subpartition_0334 partition(p_range_2);
--step10: 清空指定一级分区数据; expect:成功
alter table t_subpartition_0334 truncate partition p_range_1;
--step11: 清空指定一级分区数据; expect:成功
alter table t_subpartition_0334 truncate partition p_range_2;
--step12: 查询指定一级分区数据; expect:成功,无数据
select * from t_subpartition_0334 partition(p_range_1);
--step13: 查询指定一级分区数据; expect:成功,无数据
select * from t_subpartition_0334 partition(p_range_2);

--test3: truncate  subpartition
--step14: 插入数据; expect:成功
insert into t_subpartition_0334 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step15: 查询指定一级分区数据; expect:成功,有数据
select * from t_subpartition_0334 subpartition(p_range_2_subpartdefault1);
--step16: 清空多个二级分区数据; expect:合理报错
alter table t_subpartition_0334 truncate subpartition p_hash_3_2,p_range_2_subpartdefault1;
--step17: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0334 truncate subpartition p_range_2_subpartdefault1;
--step18: 查询指定一级分区数据; expect:成功,无数据
select * from t_subpartition_0334 subpartition(p_range_2_subpartdefault1);

--test4: delete table
--step19: 插入数据; expect:成功
insert into t_subpartition_0334 values(-11,11,1,1),(4,41,4,4),(5,54,5,5),(28,87,8,8),(39,19,9,9);
insert into t_subpartition_0334 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0334 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step20: 查询数据; expect:成功,有数据
select * from t_subpartition_0334;
--step21: 查询指定分区数据; expect:成功,有数据
select * from t_subpartition_0334 subpartition(p_range_2_subpartdefault1);
--step22: 删除表数据; expect:成功
delete from  t_subpartition_0334;
--step23: 查询数据; expect:成功,无数据
select * from t_subpartition_0334;
--step24: 查询指定分区数据; expect:成功,无数据
select * from t_subpartition_0334 subpartition(p_range_2_subpartdefault1);

--test5: delete  where
--step25: 插入数据; expect:成功
insert into t_subpartition_0334 values(-11,11,1,1),(4,41,4,4),(5,54,5,5),(28,87,8,8),(39,19,9,9);
insert into t_subpartition_0334 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0334 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step26: 查询数据; expect:成功,有数据
select * from t_subpartition_0334;
--step27: 删除指定条件的数据; expect:成功
delete from  t_subpartition_0334 where col_1 >18 ;
delete from  t_subpartition_0334 where col_2 <10 and col_3>5;
delete from  t_subpartition_0334 where col_2 <50 and col_3>5;
--step28: 查询数据; expect:成功,数据减少
select * from t_subpartition_0334;
--step29: 删除指定条件的数据; expect:成功
delete  t_subpartition_0334 where col_2-100>10;
delete  t_subpartition_0334 where col_2-100>10;
delete  t_subpartition_0334 where col_2/5>1;
--step30: 查询数据; expect:成功,数据减少
select * from t_subpartition_0334;
--step31: 查询数据; expect:成功
select * from t_subpartition_0334 subpartition(p_range_2_subpartdefault1);

--step32: 清理环境; expect:成功
drop table if exists t_subpartition_0334;
drop tablespace if exists ts_subpartition_0334;