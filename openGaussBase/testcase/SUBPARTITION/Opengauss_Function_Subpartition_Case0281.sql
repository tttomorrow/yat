-- @testpoint: range_range二级分区表：insert  on duplicate key update/with_query insert字段相同/字段数目不符，部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0281;
drop tablespace if exists ts_subpartition_0281;
create tablespace ts_subpartition_0281 relative location 'subpartition_tablespace/subpartition_tablespace_0281';

--test1: insert --insert  on duplicate key update
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0281
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0281
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
--step3: 创建索引; expect:成功
create unique index on t_subpartition_0281(col_1);
--step4: 插入数据; expect:成功
insert into t_subpartition_0281 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0281 subpartition (p_range_1_2);
--step6: 插入重复数据更新一级分区键; expect:合理报错
insert into t_subpartition_0281 values(1,11,1,1) on duplicate key update col_1=10;
--step7: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0281 values(1,11,1,1) on duplicate key update col_2=10;
--step8: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0281 values(1,11,1,1) on duplicate key update col_2=1;
--step9: 查询指定二级分区数据; expect:成功，数据更新
select * from t_subpartition_0281 subpartition (p_range_1_2);

--test2: insert --with_query  insert(字段相同)
--step10: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0281;
create   table if not exists t_subpartition_0281
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0281
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
--step11: 创建普通表; expect:成功
drop table if exists t_subpartition_0281_01;
create   table if not exists t_subpartition_0281_01
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0281;
--step12: 插入数据; expect:成功
insert into t_subpartition_0281_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step13: 查询临时表数据，查询到二级分区表; expect:成功
with with_t as (select 1,11,1,1) insert into t_subpartition_0281 (select * from with_t);
--step14: 查询普通表的数据，插入到二级分区表; expect:成功
insert into t_subpartition_0281 select * from t_subpartition_0281_01;
--step15: 二级分区表插入数据; expect:成功
insert into t_subpartition_0281 values(15,9,1,1);

--test3: insert --with_query  insert(字段数目不符)
--step16: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0281;
create   table if not exists t_subpartition_0281
(
    col_1 int ,
    col_2 int  ,
	col_3 int 
)tablespace ts_subpartition_0281
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
--step17: 创建普通表; expect:成功
drop table if exists t_subpartition_0281_01;
create   table if not exists t_subpartition_0281_01
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0281;
--step18: 普通表插入数据; expect:成功
insert into t_subpartition_0281_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step19: 查询临时表所有数据，插入到二级分区表; expect:合理报错
with with_t as (select 1,11,1,1) insert into t_subpartition_0281 (select * from with_t);
--step20: 查询普通表的所有数据，插入到二级分区表; expect:合理报错
insert into t_subpartition_0281 select * from t_subpartition_0281_01;
--step21: 查询普通表的指定2列数据，插入到二级分区表; expect:成功
insert into t_subpartition_0281 select col_1,col_2 from t_subpartition_0281_01;
--step22: 查询普通表的指定3列数据，插入到二级分区表; expect:成功
insert into t_subpartition_0281 select col_1,col_2,col_3 from t_subpartition_0281_01;
--step23: 二级分区表插入数据; expect:成功
insert into t_subpartition_0281 values(15,9,1);

--step24: 清理环境; expect:成功
drop table if exists t_subpartition_0281;
drop table if exists t_subpartition_0281_01;
drop tablespace if exists ts_subpartition_0281;