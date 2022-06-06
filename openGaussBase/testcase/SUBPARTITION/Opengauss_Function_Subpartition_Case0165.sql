-- @testpoint: list_hash二级分区表：delete

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0165;
drop tablespace if exists ts_subpartition_0165;
create tablespace ts_subpartition_0165 relative location 'subpartition_tablespace/subpartition_tablespace_0165';
drop tablespace if exists ts_subpartition_0165_01;
create tablespace ts_subpartition_0165_01 relative location 'subpartition_tablespace/subpartition_tablespace_0165_01';
--test1: delete table
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0165
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0165
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
    subpartition p_hash_2_4 tablespace ts_subpartition_0165_01 ,
    subpartition p_hash_2_5
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 tablespace ts_subpartition_0165_01
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
insert into t_subpartition_0165 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0165 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0165 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0165 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0165 values(-8,18,1);
--step4: 查询数据; expect:成功
select * from t_subpartition_0165;
--step5: 查询指定二级分区数据; expect:成功,5条数据
select * from t_subpartition_0165 subpartition(p_list_3_subpartdefault1);
--step6: 查询指定二级分区数据; expect:成功,1条数据
select * from t_subpartition_0165 subpartition(p_hash_5_1);
--step7: 删除表数据; expect:成功
delete from  t_subpartition_0165;
--step8: 查询表数据; expect:成功,0条数据
select * from t_subpartition_0165;
--step9: 查询指定二级分区数据; expect:成功,0条数据
select * from t_subpartition_0165 subpartition(p_hash_5_1);
--step10: 查询指定二级分区数据; expect:成功,0条数据
select * from t_subpartition_0165 subpartition(p_list_3_subpartdefault1);

--test2: delete  where
--step11: 插入数据; expect:成功
insert into t_subpartition_0165 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0165 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0165 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0165 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0165 values(-8,18,1);
--step12: 删除指定条件的数据; expect:成功
delete from  t_subpartition_0165 where col_1 >18 ;
--step13: 删除指定条件的数据; expect:成功
delete from  t_subpartition_0165 where col_2 <10 and col_3>5;
--step14: 删除指定条件的数据; expect:成功
delete from  t_subpartition_0165 where col_2 <50 and col_3>5;
--step15: 查询数据; expect:成功,10条数据
select * from t_subpartition_0165;
--step16: 删除指定条件的数据; expect:成功
delete  t_subpartition_0165 where col_2-100>10;
--step17: 删除指定条件的数据; expect:成功
delete  t_subpartition_0165 where col_2-100>10;
--step18: 删除指定条件的数据; expect:成功
delete  t_subpartition_0165 where col_2/5>1;
--step19: 查询数据; expect:成功,4条数据
select * from t_subpartition_0165 ;

--step20: 清理环境; expect:成功
drop table if exists t_subpartition_0165;
drop tablespace if exists ts_subpartition_0165;