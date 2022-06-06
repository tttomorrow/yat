-- @testpoint: list_hash二级分区表：分区键的字段类型与指定类型不符/相符,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0153;
drop tablespace if exists ts_subpartition_0153;
create tablespace ts_subpartition_0153 relative location 'subpartition_tablespace/subpartition_tablespace_0153';
--step2: 创建二级分区表,二级分区键的字段类型与指定类型不符; expect:合理报错
create table if not exists t_subpartition_0153
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int ,
    col_19 date ,
    col_20 int
)
tablespace ts_subpartition_0153
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values ( to_date('2018-11-01','yyyy-mm-dd' ),to_date('2018-11-02','yyyy-mm-dd' ),to_date('2018-11-03','yyyy-mm-dd' ))
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values ( to_date('2019-11-01','yyyy-mm-dd' ))
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values ( to_date('2020-11-01','yyyy-mm-dd' )),
  partition p_list_4 values ( to_date('2021-11-01','yyyy-mm-dd' ))
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values ( to_date('2022-11-01','yyyy-mm-dd' ))
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step3: 创建二级分区表,分区键的字段类型与指定类型相符; expect:成功
drop table if exists t_subpartition_0153;
create table if not exists t_subpartition_0153
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int ,
    col_19 date ,
    col_20 int
)
tablespace ts_subpartition_0153
partition by list (col_19) subpartition by hash (col_1)
(
  partition p_list_1 values ( to_date('2018-11-01','yyyy-mm-dd' ),to_date('2018-11-02','yyyy-mm-dd' ),to_date('2018-11-03','yyyy-mm-dd' ))
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3 
  ),
  partition p_list_2 values ( to_date('2019-11-01','yyyy-mm-dd' ))
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values ( to_date('2020-11-01','yyyy-mm-dd' )),
  partition p_list_4 values ( to_date('2021-11-01','yyyy-mm-dd' ))
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  ),
  partition p_list_6 values ( to_date('2022-11-01','yyyy-mm-dd' ))
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3 
  )
) enable row movement ;
--step4: 插入数据; expect:成功
insert into t_subpartition_0153 values(1,1,1,1,'2018-05-08');
--step5: 查询数据; expect:成功
select * from t_subpartition_0153 subpartition(p_hash_1_1);
--step6: 查询数据; expect:成功
select * from t_subpartition_0153 subpartition(p_hash_1_2);
--step7: 查询数据; expect:成功
select * from t_subpartition_0153 subpartition(p_hash_5_1);

--step8: 创建二级分区表,分区键的字段类型与指定类型相符; expect:成功
drop table if exists t_subpartition_0153;
create table t_subpartition_0153
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int,
    col_19 date
)
partition by list (col_2) subpartition by hash (col_19)
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
--step9: 插入数据; expect:成功
insert into t_subpartition_0153 values(1,21,1,1,'2018-05-08');
--step10: 查询数据; expect:成功
select * from t_subpartition_0153 subpartition(p_hash_4_1);
--step11: 更新数据; expect:成功
update t_subpartition_0153 set col_19='2019-05-08'where col_19='2018-05-08';
 --step12: 查询数据; expect:成功
select * from t_subpartition_0153 subpartition(p_hash_4_1);
--step13: 删除数据; expect:成功
delete t_subpartition_0153 where col_19 = '2019-05-08';
--step14: 查询数据; expect:成功
select * from t_subpartition_0153 subpartition(p_hash_4_1);
--step15: 查询数据; expect:成功
select * from t_subpartition_0153 ;

--step16: 清理环境; expect:成功
drop table if exists t_subpartition_0153;
drop tablespace if exists ts_subpartition_0153;