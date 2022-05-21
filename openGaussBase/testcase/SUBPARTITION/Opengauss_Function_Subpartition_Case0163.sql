-- @testpoint: list_hash二级分区表：with_query insert字段类型不符/update更新

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0163;
drop table if exists t_subpartition_0163_01;
drop tablespace if exists ts_subpartition_0163;
create tablespace ts_subpartition_0163 relative location 'subpartition_tablespace/subpartition_tablespace_0163';
drop tablespace if exists ts_subpartition_0163_01;
create tablespace ts_subpartition_0163_01 relative location 'subpartition_tablespace/subpartition_tablespace_0163_01';

--test1: insert --with_query  insert(字段类型不符)
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0163
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0163
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
--step3: 创建普通表; expect:成功
drop table if exists t_subpartition_0163_01;
create table if not exists t_subpartition_0163_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0163;
--step4: 普通表插入数据; expect:成功
insert into t_subpartition_0163_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 查询临时表数据,插入到二级分区表; expect:成功
with with_t as (select 1,11,1,1) insert into t_subpartition_0163 (select * from with_t);
--step6: 查询普通表的数据,插入到二级分区表; expect:成功
insert into t_subpartition_0163 select * from t_subpartition_0163_01;
--step7: 查询二级分区表数据; expect:成功
select * from t_subpartition_0163;

--test2: update--更新非分区列
--step8: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0163;
create table if not exists t_subpartition_0163
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0163
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
    subpartition p_hash_2_4 tablespace ts_subpartition_0163_01 ,
    subpartition p_hash_2_5 
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 tablespace ts_subpartition_0163_01
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
insert into t_subpartition_0163 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0163 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0163 values(21,11,1,1),(25,15,5,5),(28,81,8,8),(-29,31,9,9);
insert into t_subpartition_0163 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0163 values(-8,18,1);
--step10: 更新非分区列的数据为数字; expect:成功
update t_subpartition_0163 set col_4=80 where col_1=5; 
--step11: 查询二级分区数据; expect:成功
select * from t_subpartition_0163 subpartition(p_hash_4_1);
--step12: 更新非分区列的数据为一级分区键数据; expect:成功
update t_subpartition_0163 set col_4=col_1 where col_1<5; 
--step13: 查询数据; expect:成功,col_4=col_1
select * from t_subpartition_0163 where col_1<5;
--step14: 更新非分区列的数据为一级分区键数据+二级分区键数据; expect:成功
update t_subpartition_0163 set col_4=col_1+ col_2 where col_1<5;
--step15: 查询数据; expect:成功,col_4=col_1+ col_2
select * from t_subpartition_0163 where col_1<5;

--test3: update--更新至一级分区外
--step16: 查询二级分区数据; expect:成功,3条数据
select * from t_subpartition_0163 subpartition(p_list_3_subpartdefault1);
--step17: 更新分区列的数据至原分区外; expect:成功
update t_subpartition_0163 set col_1=80,col_2=8 where col_1=15;
--step18: 查询二级分区数据; expect:成功,2条数据
select * from t_subpartition_0163 subpartition(p_hash_5_1);
--step19: 查询二级分区数据; expect:成功,2条数据
select * from t_subpartition_0163 subpartition(p_list_3_subpartdefault1);


--test4: update--更新至一级分区内-二级分区外
--step20: 查询二级分区数据; expect:成功
select * from t_subpartition_0163 subpartition(p_hash_1_1);
--step21: 查询二级分区数据; expect:成功
select * from t_subpartition_0163 subpartition(p_hash_1_2);
--step22: 查询二级分区数据; expect:成功
select * from t_subpartition_0163 subpartition(p_hash_1_3);
--step23: 更新分区列的数据至一级分区内-二级分区外; expect:成功
update t_subpartition_0163 set col_2=-3 where col_1=-8;
--step24: 查询二级分区数据; expect:成功
select * from t_subpartition_0163 subpartition(p_hash_1_1);
--step25: 查询二级分区数据; expect:成功
select * from t_subpartition_0163 subpartition(p_hash_1_2);
--step26: 查询二级分区数据; expect:成功
select * from t_subpartition_0163 subpartition(p_hash_1_3);

--test5: update--更新至一级分区内-二级分区内
--step27: 查询二级分区数据; expect:成功,2条数据
select * from t_subpartition_0163 subpartition(p_hash_5_1);
--step28: 更新分区列的数据至一级分区内-二级分区内; expect:成功
update t_subpartition_0163 set col_2=-40 where col_2=-31;
--step29: 查询数据; expect:成功,数据已更新
select * from t_subpartition_0163 subpartition(p_hash_5_1);

--step30: 清理环境; expect:成功
drop table if exists t_subpartition_0163;
drop table if exists t_subpartition_0163_01;
drop tablespace if exists ts_subpartition_0163;
drop tablespace if exists ts_subpartition_0163_01;