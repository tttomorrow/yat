-- @testpoint: range_range二级分区表：with_query insert字段类型不符/update更新

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0282;
drop table if exists t_subpartition_0282_01;
drop tablespace if exists ts_subpartition_0282;
create tablespace ts_subpartition_0282 relative location 'subpartition_tablespace/subpartition_tablespace_0282';

--test1: insert --with_query  insert(字段类型不符)
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0282
(
    col_1 int ,
    col_2 int  ,
	col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0282
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
drop table if exists t_subpartition_0282_01;
create   table if not exists t_subpartition_0282_01
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0282;
--step4: 普通表插入数据; expect:成功
insert into t_subpartition_0282_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 查询临时表数据，插入到二级分区表; expect:成功
with with_t as (select 1,11,1,1) insert into t_subpartition_0282 (select * from with_t);
--step6: 查询普通表的数据，插入到二级分区表; expect:成功
insert into t_subpartition_0282 select * from t_subpartition_0282_01;
--step7: 查询二级分区表数据; expect:成功，有数据
select * from t_subpartition_0282;

--test2: update--更新非分区列
--step8: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0282;
create   table if not exists t_subpartition_0282
(
    col_1 int ,
    col_2 int  ,
	col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0282
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
--step9: 插入数据; expect:成功
insert into t_subpartition_0282 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);

--step10: 更新非分区列的数据为数字; expect:成功
update t_subpartition_0282 set col_4=80 where col_1=4;
--step11: 更新非分区列的数据为一级分区键数据; expect:成功
update t_subpartition_0282 set col_4=col_1 where col_1<5;
--step12: 查询数据; expect:成功，col_4=col_1
select * from t_subpartition_0282 where col_1<5;
--step13: 更新非分区列的数据为一级分区键数据+二级分区键数据; expect:成功
update t_subpartition_0282 set col_4=col_1+ col_2 where col_1<5;
--step14: 查询数据; expect:成功,col_4=col_1+ col_2
select * from t_subpartition_0282 where col_1<5;

--test3: update--更新至一级分区外
--step15: 查询数据; expect:成功，5条数据
select * from t_subpartition_0282 subpartition(p_range_1_2);
--step16: 更新分区列的数据至原分区外; expect:成功
update t_subpartition_0282 set col_1=15,col_2=8 where col_1=1; 
--step17: 查询数据; expect:成功，4条数据
select * from t_subpartition_0282 subpartition(p_range_1_2);
--step18: 查询数据; expect:成功，1条数据
select * from t_subpartition_0282 partition(p_range_2);

--test4: update--更新至一级分区内-二级分区内
--step19: 更新分区列的数据至一级分区内-二级分区内; expect:成功
update t_subpartition_0282 set col_1=3,col_2=80 where col_1=9;
--step20: 查询数据; expect:成功,数据更新
select * from t_subpartition_0282 subpartition(p_range_1_2);

--test5: update--更新至一级分区内-二级分区外
--step21: 更新数据; expect:成功
update t_subpartition_0282 set col_1=18,col_2=8 where col_1=3;
--step22: 查询数据; expect:成功，3条数据
select * from t_subpartition_0282 subpartition(p_range_1_2);
--step23: 查询数据; expect:成功，两条数据
select * from t_subpartition_0282 subpartition(p_range_2_2);

--step24: 清理环境; expect:成功
drop table if exists t_subpartition_0282;
drop table if exists t_subpartition_0282_01;
drop tablespace if exists ts_subpartition_0282;