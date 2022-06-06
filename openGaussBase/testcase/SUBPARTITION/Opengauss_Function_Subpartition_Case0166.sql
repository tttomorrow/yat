-- @testpoint: list_hash二级分区表：select

--test1: select partition/subpartition for
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0166;
drop tablespace if exists ts_subpartition_0166;
create tablespace ts_subpartition_0166 relative location 'subpartition_tablespace/subpartition_tablespace_0166';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0166
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0166
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0166 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0166 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0166 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0166 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0166 values(-8,18,1);
--step4: 查询一级分区数据; expect:成功
select * from t_subpartition_0166 partition for (5);
--step5: 查询二级分区数据; expect:成功
select * from t_subpartition_0166 subpartition for (29,9);

--test2: select 各种组合
--step6: 查询数据：subpartition/order by/desc; expect:成功
select * from t_subpartition_0166 subpartition(p_list_3_subpartdefault1) order by 1 desc,2;
--step7: 查询数据：subpartition/order by/desc/limit; expect:成功
select * from t_subpartition_0166 subpartition(p_list_3_subpartdefault1) order by 1 desc,2 limit 2,5;
--step8: 查询数据：subpartition/order by/desc/limit/offset; expect:成功
select * from t_subpartition_0166 subpartition(p_list_3_subpartdefault1) order by 1 desc,2 limit 2 offset 3;
--step9: 查询数据：partition/order by/desc/limit/offset; expect:成功
select col_2 from t_subpartition_0166 partition(p_list_1) order by 1 desc limit 2 offset 3;
--step10: 自连接查询数据; expect:成功
select * from t_subpartition_0166  a,t_subpartition_0166 b  where a.col_1=b.col_2 and  a.col_1 >10;
--step11: 子查询查询数据; expect:成功
select * from (select * from t_subpartition_0166 subpartition(p_list_3_subpartdefault1))a,((select * from t_subpartition_0166 subpartition(p_hash_1_2))) b  where a.col_1=b.col_2;

--step12: 清理环境; expect:成功
drop table if exists t_subpartition_0166;
drop tablespace if exists ts_subpartition_0166;