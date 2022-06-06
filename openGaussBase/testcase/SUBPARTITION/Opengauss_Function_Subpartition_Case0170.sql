-- @testpoint: list_hash二级分区表：序列--非分区列序列

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0170;
drop tablespace if exists ts_subpartition_0170;
create tablespace ts_subpartition_0170 relative location 'subpartition_tablespace/subpartition_tablespace_0170';

--test1: 序列--非分区列序列
--step2: 创建序列; expect:成功
drop sequence if exists seql_subpartition_0170;
create sequence seql_subpartition_0170 cache 100;
--step3: 创建二级分区表,将序列值作为非分区列的默认值,使该字段具有唯一标识属性; expect:成功
create table if not exists t_subpartition_0170
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int not null default nextval('seql_subpartition_0170')
)tablespace ts_subpartition_0170
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
--step4: 指定序列与列的归属关系; expect:成功
alter sequence seql_subpartition_0170 owned by t_subpartition_0170.col_4;
--step5: 插入数据; expect:成功
insert into t_subpartition_0170 values(21,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0170 values(11,1,1),(1,1,4),(15,5,5),(81,8,8),(19,9,9);
insert into t_subpartition_0170 values(18,1,1),(48,1,4),(57,5,5),(87,8,8),(95,9,9);

--step6: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0170 subpartition(p_hash_5_1);
--step7: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0170 subpartition(p_hash_4_1);
--step8: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0170 truncate subpartition p_hash_5_1;
--step9: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0170 subpartition(p_hash_5_1);
--step10: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0170 subpartition(p_hash_4_1);
--step11: 插入数据; expect:成功
insert into t_subpartition_0170 values(81,1,1),(94,1,4),(445,5,5),(8768,8,8),(7869,9,9);
--step12: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0170 subpartition(p_list_3_subpartdefault1);
--step13: 查询表数据; expect:成功,有数据
select * from t_subpartition_0170;

--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0170;
drop tablespace if exists ts_subpartition_0170;