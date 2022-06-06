-- @testpoint: list_hash二级分区表：分区数1个/分区键非顺序指定,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0152;
drop tablespace if exists ts_subpartition_0152;
create tablespace ts_subpartition_0152 relative location 'subpartition_tablespace/subpartition_tablespace_0152';
drop tablespace if exists ts_subpartition_0152_01;
create tablespace ts_subpartition_0152_01 relative location 'subpartition_tablespace/subpartition_tablespace_0152_01';

--test1: 分区数--1个
--step2: 创建二级分区表,一级分区数和二级分区数各1个; expect:成功
create table if not exists t_subpartition_0152
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0152
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 
)
) disable row movement;
--step3: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable ,boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0152') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0152')) b where a.parentid = b.oid order by a.relname;

--step4: 插入数据; expect:成功
insert into t_subpartition_0152 values(-8,-10,1);
 --step5: 查询数据; expect:成功
select * from t_subpartition_0152;
--step6: 查询二级分区数据; expect:成功
select * from t_subpartition_0152 subpartition (p_hash_1_1);

--step7: 创建二级分区表,一级分区数1个，二级分区数0; expect:成功
drop table if exists t_subpartition_0152;
create table if not exists t_subpartition_0152
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0152
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 ) tablespace ts_subpartition_0152_01
 ) enable row movement;
--step8: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0152') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0152')) b where a.parentid = b.oid order by a.relname;
--step9: 插入数据; expect:成功
insert into t_subpartition_0152 values(-1,-1,-1,1),(-5,5,5,5),(-8,8,8,8),(-9,9,9,9);
--step10: 插入不在分区范围内的数据; expect:合理报错
insert into t_subpartition_0152 values(11,1,1,1),(15,5,5,5),(18,8,8,8),(19,9,9,9);
--step11: 插入不在分区范围内的数据; expect:合理报错
insert into t_subpartition_0152 values(-21,1,1,1),(-25,5,5,5),(-28,8,8,8),(-29,9,9,9);
--step12: 查询一级分区数据; expect:成功
select * from t_subpartition_0152 partition(p_list_1);
--step13: 查询二级分区default数据; expect:成功
select * from t_subpartition_0152 subpartition(p_list_1_subpartdefault1);

--test2: 分区键--非顺序指定
--step14: 创建二级分区表,一级分区键非顺序指定; expect:成功
drop table if exists t_subpartition_0152;
create table if not exists t_subpartition_0152
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int ,
    col_19 int
)
tablespace ts_subpartition_0152
partition by list (col_19) subpartition by hash (col_2)
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
--step15: 创建二级分区表,分区键非顺序指定; expect:成功
drop table if exists t_subpartition_0152;
create table t_subpartition_0152
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by list (col_2) subpartition by hash (col_1)
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
--step16: 插入数据; expect:成功
insert into t_subpartition_0152 values(1,21,1,1);
--step17: 查询指定二级分区数据; expect:成功
select *  from t_subpartition_0152 subpartition(p_hash_4_1);
--step18: 更新指定二级分区数据; expect:成功
update t_subpartition_0152 set col_2=39 where col_1=1;
--step19: 查询指定二级分区数据; expect:成功
select *  from t_subpartition_0152 subpartition(p_hash_4_1);
--step20: 更新指定二级分区数据; expect:成功
update t_subpartition_0152 set col_1=80 where col_2=39;
--step21: 查询指定二级分区数据; expect:成功
select *  from t_subpartition_0152 subpartition(p_hash_4_1);
--step22: 查询指定二级分区数据; expect:成功
select *  from t_subpartition_0152 subpartition(p_hash_5_1);

--step23: 清理环境; expect:成功
drop table if exists t_subpartition_0152;
drop tablespace if exists ts_subpartition_0152;