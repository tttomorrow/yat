-- @testpoint: list_range二级分区表：分区键的字段类型与指定类型不符/相符,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0096;
drop tablespace if exists ts_subpartition_0096;
create tablespace ts_subpartition_0096 relative location 'subpartition_tablespace/subpartition_tablespace_0096';
--step2: 创建二级分区表,二级分区键的字段类型与指定类型不符; expect:合理报错
create table if not exists t_subpartition_0096
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int ,
    col_19 date ,
    col_20 int
)
tablespace ts_subpartition_0096
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_2 values less than( to_date('2019-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_3 values less than( to_date('2020-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_4 values less than( to_date('2021-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_5 values less than( to_date('2022-11-01','yyyy-mm-dd' ))
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
   partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_2 values less than( to_date('2019-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_3 values less than( to_date('2020-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_4 values less than( to_date('2021-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_5 values less than( to_date('2022-11-01','yyyy-mm-dd' ))
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_2 values less than( to_date('2019-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_3 values less than( to_date('2020-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_4 values less than( to_date('2021-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_5 values less than( to_date('2022-11-01','yyyy-mm-dd' ))
   ),
   partition p_list_7 values(default)
) enable row movement;
--step3: 创建二级分区表,分区键的字段类型与指定类型相符; expect:成功
drop table if exists t_subpartition_0096;
create table if not exists t_subpartition_0096
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int ,
    col_19 date ,
    col_20 int
)
tablespace ts_subpartition_0096
partition by list (col_1) subpartition by range (col_19)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_2 values less than( to_date('2019-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_3 values less than( to_date('2020-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_4 values less than( to_date('2021-11-01','yyyy-mm-dd' )),
    subpartition p_range_1_5 values less than( to_date('2022-11-01','yyyy-mm-dd' ))
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
   partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_2 values less than( to_date('2019-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_3 values less than( to_date('2020-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_4 values less than( to_date('2021-11-01','yyyy-mm-dd' )),
    subpartition p_range_4_5 values less than( to_date('2022-11-01','yyyy-mm-dd' ))
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( to_date('2018-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_2 values less than( to_date('2019-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_3 values less than( to_date('2020-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_4 values less than( to_date('2021-11-01','yyyy-mm-dd' )),
    subpartition p_range_6_5 values less than( to_date('2022-11-01','yyyy-mm-dd' ))
   ),
   partition p_list_7 values(default)
) enable row movement;
--step4: 插入数据; expect:成功
insert into t_subpartition_0096 values(1,1,1,1,'2018-05-08');
--step5: 查询一级数据; expect:成功
select * from t_subpartition_0096 partition(p_list_2);
--step6: 查询二级数据; expect:成功
select * from t_subpartition_0096 subpartition(p_list_2_subpartdefault1);
--step7: 插入数据; expect:成功
insert into t_subpartition_0096 values(42,1,1,1,'2018-05-08');
--step8: 查询二级分区数据数据; expect:成功
select * from t_subpartition_0096 subpartition(p_range_6_1);
--step9: 查询二级分区数据数据; expect:成功
select * from t_subpartition_0096 subpartition(p_range_6_2);
--step10: 插入数据; expect:成功
insert into t_subpartition_0096 values(42,1,1,1,'2019-11-01');
--step11: 查询二级分区数据数据; expect:成功
select * from t_subpartition_0096 subpartition(p_range_6_2);
--step12: 查询二级分区数据数据; expect:成功
select * from t_subpartition_0096 subpartition(p_range_6_3);

--step13: 清理环境; expect:成功
drop table if exists t_subpartition_0096;
drop tablespace if exists ts_subpartition_0096;