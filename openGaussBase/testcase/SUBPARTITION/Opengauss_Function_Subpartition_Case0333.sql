-- @testpoint: range_hash二级分区表：with_query insert/update更新,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0333;
drop tablespace if exists ts_subpartition_0333;
create tablespace ts_subpartition_0333 relative location 'subpartition_tablespace/subpartition_tablespace_0333';

--test1: insert --with_query  insert(字段数目不符)
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0333
(
    col_1 int ,
    col_2 int ,
    col_3 int
)tablespace ts_subpartition_0333
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
    subpartition t_subpartition_0333
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 创建普通表; expect:成功
drop table if exists t_subpartition_0333_01;
create table if not exists t_subpartition_0333_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0333;
--step4: 普通表插入数据; expect:成功
insert into t_subpartition_0333_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 查询临时表数据,插入到二级分区表; expect:合理报错
with with_t as (select 1,11,1,1) insert into t_subpartition_0333 (select * from with_t);
--step6: 查询普通表的所有数据,插入到二级分区表; expect:合理报错
insert into t_subpartition_0333 select * from t_subpartition_0333_01;
--step7: 查询普通表的2列数据,插入到二级分区表; expect:成功
insert into t_subpartition_0333 select col_1,col_2 from t_subpartition_0333_01;
--step8: 查询普通表的3列数据,插入到二级分区表; expect:成功
insert into t_subpartition_0333 select col_1,col_2,col_3 from t_subpartition_0333_01;
--step9: 查询指定分区数据; expect:成功
select * from t_subpartition_0333 partition(p_range_2) where col_3 is null;
--step10: 查询指定条件数据; expect:成功
select aa.col_1,count(aa.col_3)  from t_subpartition_0333 partition(p_range_2) aa,t_subpartition_0333 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2 /10 >5 group by aa.col_1;
--step11: 查询指定条件数据; expect:成功
select aa.col_1,sum(aa.col_3)  from t_subpartition_0333 partition(p_range_2) aa,t_subpartition_0333 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2/10 >5 group by aa.col_1;
--step12: 查询指定条件数据; expect:成功
select aa.col_1,sum(aa.col_3)  from t_subpartition_0333 partition(p_range_2) aa,t_subpartition_0333 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2/10 >5 and aa.col_3 is not null group by aa.col_1;
--step13: 查询指定条件数据; expect:成功
select *  from t_subpartition_0333 partition(p_range_2) aa,t_subpartition_0333 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2 /10 >5 and aa.col_3 is not null ;
--step14: 二级分区表插入数据; expect:成功
insert into t_subpartition_0333 values(15,9,1);
--step15: 查询指定条件数据; expect:成功
select aa.col_1,min(bb.col_2)  from t_subpartition_0333 partition(p_range_2) aa,t_subpartition_0333 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_3 is not null group by aa.col_1;

--test2: insert --with_query  insert(字段类型不符)
--step16: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0333;
create table if not exists t_subpartition_0333
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0333
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step17: 创建普通表; expect:成功
drop table if exists t_subpartition_0333_01;
create table if not exists t_subpartition_0333_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0333;
--step18: 普通表插入数据; expect:成功
insert into t_subpartition_0333_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step19: 查询临时表数据,插入到二级分区表; expect:成功
with with_t as (select 1,11,1,1) insert into t_subpartition_0333 (select * from with_t);
--step20: 查询普通表的数据,插入到二级分区表; expect:成功
insert into t_subpartition_0333 select * from t_subpartition_0333_01;
--step21: 查询二级分区表数据; expect:成功,有数据
select * from t_subpartition_0333;

--test3: update--更新非分区列
--step22: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0333;
create table if not exists t_subpartition_0333
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0333
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
    subpartition t_subpartition_0333
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step23: 插入数据; expect:成功
insert into t_subpartition_0333 values(-11,11,1,1),(4,41,4,4),(5,54,5,5),(28,87,8,8),(39,19,9,9);

--step24: 更新非分区列的数据为数字; expect:成功
update t_subpartition_0333 set col_4=80 where col_1=4;
--step25: 更新非分区列的数据为一级分区键数据; expect:成功
update t_subpartition_0333 set col_4=col_1 where col_1<5;
--step26: 查询数据; expect:成功,col_4=col_1
select * from t_subpartition_0333 where col_1<5;
--step27: 更新非分区列的数据为一级分区键数据+二级分区键数据; expect:成功
update t_subpartition_0333 set col_4=col_1+ col_2 where col_1<5;
--step28: 查询数据; expect:成功,col_4=col_1+ col_2
select * from t_subpartition_0333 where col_1<5;

--test4: update--更新至一级分区外
--step29: 查询数据; expect:成功,2条数据
select * from t_subpartition_0333 subpartition(p_range_2_subpartdefault1);
--step30: 更新分区列的数据至原分区外; expect:成功
update t_subpartition_0333 set col_1=80,col_2=8 where col_1=4;
--step31: 查询数据; expect:成功,1条数据
select * from t_subpartition_0333 subpartition(p_range_2_subpartdefault1);
--step32: 查询数据; expect:成功,1条数据
select * from t_subpartition_0333 subpartition(p_range_5_subpartdefault1);

--step33: 清理环境; expect:成功
drop table if exists t_subpartition_0333;
drop table if exists t_subpartition_0333_01;
drop tablespace if exists ts_subpartition_0333;