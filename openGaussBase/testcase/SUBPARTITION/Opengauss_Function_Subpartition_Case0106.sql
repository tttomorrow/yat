-- @testpoint: list_range二级分区表：with_query insert字段类型不符/update更新

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0106;
drop table if exists t_subpartition_0106_01;
drop tablespace if exists ts_subpartition_0106;
create tablespace ts_subpartition_0106 relative location 'subpartition_tablespace/subpartition_tablespace_0106';

--test1: insert --with_query  insert(字段类型不符)
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0106
(
    col_1 int  unique,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0106
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step3: 创建普通表; expect:成功
drop table if exists t_subpartition_0106_01;
create table if not exists t_subpartition_0106_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0106;
--step4: 普通表插入数据; expect:成功
insert into t_subpartition_0106_01 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 查询临时表数据，插入到二级分区表; expect:成功
with with_t as (select 1,11,1,1) insert into t_subpartition_0106 (select * from with_t);
--step6: 查询普通表的数据，插入到二级分区表; expect:成功
insert into t_subpartition_0106 select * from t_subpartition_0106_01;
--step7: 查询二级分区表数据; expect:成功
select * from t_subpartition_0106;

--test2: update--更新非分区列
--step8: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0106;
create table if not exists t_subpartition_0106
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0106
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step9: 插入数据; expect:成功
insert into t_subpartition_0106 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0106 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0106 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0106 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0106 values(-8,18,1);
--step10: 更新非分区列的数据为数字; expect:成功
update t_subpartition_0106 set col_4=80 where col_1=5; 
--step11: 查询二级分区数据; expect:成功，4条数据
select * from t_subpartition_0106 subpartition(p_list_2_subpartdefault1);
--step12: 更新非分区列的数据为一级分区键数据; expect:成功
update t_subpartition_0106 set col_4=col_1 where col_1<5; 
--step13: 查询二级分区数据; expect:成功，col_4=col_1
select * from t_subpartition_0106 subpartition(p_range_1_1);
--step14: 查询二级分区数据; expect:成功，col_4=col_1
select * from t_subpartition_0106 subpartition(p_range_1_3);
--step15: 更新非分区列的数据为一级分区键数据+二级分区键数据; expect:成功
update t_subpartition_0106 set col_4=col_1+ col_2 where col_1<5;
--step16: 查询二级分区数据; expect:成功，col_4=col_1+ col_2
select * from t_subpartition_0106 subpartition(p_range_1_4);
--step17: 查询二级分区数据; expect:成功，col_4=col_1+ col_2
select * from t_subpartition_0106 subpartition(p_range_1_5);

--test3: update--更新至一级分区外
--step18: 查询二级分区数据; expect:成功，4条数据
select * from t_subpartition_0106 subpartition(p_list_2_subpartdefault1);
--step19: 更新分区列的数据至原分区外; expect:成功
update t_subpartition_0106 set col_1=80,col_2=8 where col_1=5;
--step20: 查询二级分区数据; expect:成功，3条数据
select * from t_subpartition_0106 subpartition(p_list_2_subpartdefault1);
--step21: 查询二级分区数据; expect:成功，2条数据
select * from t_subpartition_0106 subpartition(p_list_7_subpartdefault1);

--test4: update--更新至一级分区内-二级分区外
--step22: 查询二级分区数据; expect:成功，1条数据
select * from t_subpartition_0106 subpartition(p_range_1_5);
--step23: 查询二级分区数据; expect:成功，1条数据
select * from t_subpartition_0106 subpartition(p_range_1_4);
--step24: 更新分区列的数据至一级分区内-二级分区外; expect:成功
update t_subpartition_0106 set col_2=28 where col_2=18;
--step25: 查询二级分区数据; expect:成功，0条数据
select * from t_subpartition_0106 subpartition(p_range_1_4);
--step26: 查询二级分区数据; expect:成功，2条数据
select * from t_subpartition_0106 subpartition(p_range_1_5);

--test5: update--更新至一级分区内-二级分区内
--step27: 查询二级分区数据; expect:成功，2条数据
select * from t_subpartition_0106 subpartition(p_range_1_5);
--step28: 更新分区列的数据至一级分区内-二级分区内; expect:成功
update t_subpartition_0106 set col_2=27 where col_2=28;
--step29: 查询二级分区数据; expect:成功，2条数据,数据已更新
select * from t_subpartition_0106 subpartition(p_range_1_5);

--step30: 清理环境; expect:成功
drop table if exists t_subpartition_0106;
drop table if exists t_subpartition_0106_01;
drop tablespace if exists ts_subpartition_0106;