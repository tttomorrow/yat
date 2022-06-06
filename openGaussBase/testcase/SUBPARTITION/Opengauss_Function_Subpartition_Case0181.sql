-- @testpoint: list_hash二级分区表：生成列,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0181;
drop tablespace if exists ts_subpartition_0181;
create tablespace ts_subpartition_0181 relative location 'subpartition_tablespace/subpartition_tablespace_0181';
--step2: 创建二级分区表,一级分区列指定生成列; expect:合理报错
drop table if exists t_subpartition_0181;
create table t_subpartition_0181
(
    col_1 int generated always as(2*col_4) stored ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0181
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step3: 创建二级分区表,二级分区列指定生成列; expect:合理报错
drop table if exists t_subpartition_0181;
create table t_subpartition_0181
(
    col_1 int ,
    col_2 int generated always as(2*col_4) stored ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0181
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step4: 创建二级分区表,普通列指定生成列; expect:成功
drop table if exists t_subpartition_0181;
create table t_subpartition_0181
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int generated always as(2*col_1) stored
)
tablespace ts_subpartition_0181
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step5: 插入数据; expect:成功
insert into t_subpartition_0181 values(1,1,1),(4,4,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0181(col_1,col_2,col_3)  values(31,1,1),(34,4,4),(45,5,5),(68,8,8),(70,9,9);
--step6: 查询指定一级分区数据; expect:成功
select * from t_subpartition_0181 partition(p_list_2);
--step7: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0181 subpartition(p_hash_5_1);
--step8: 查询指定一级分区数据; expect:成功
select * from t_subpartition_0181 partition(p_list_5);

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0181;
drop tablespace if exists ts_subpartition_0181;