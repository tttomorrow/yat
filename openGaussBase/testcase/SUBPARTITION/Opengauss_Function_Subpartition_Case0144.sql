-- @testpoint: list_hash二级分区表：分区名称为普通字符串/特殊字符串,部分测试点合理报错

--test1: 分区名称-普通字符串
--step1: 创建二级分区表,分区名称为普通字符串; expect:成功
drop table if exists t_subpartition_0144;
drop tablespace if exists ts_subpartition_0144;
drop tablespace if exists ts_subpartition_0144_01;
create tablespace ts_subpartition_0144 relative location 'subpartition_tablespace/subpartition_tablespace_0144';
create tablespace ts_subpartition_0144_01 relative location 'subpartition_tablespace/subpartition_tablespace_0144_01';
create table if not exists t_subpartition_0144
(
  col_1 int primary key  using index tablespace ts_subpartition_0144_01,
  col_2 int ,
    col_3 int ,
  col_4 int
)
tablespace ts_subpartition_0144
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 (
  subpartition p_hash_1_1 ,
  subpartition p_hash_1_2 ,
  subpartition rrrrrrrrr
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
--step2: 查询分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t
where p.reltablespace=t.oid and p.relname='p_list_4' and t.spcname='ts_subpartition_0144';
--step3: 查看分区信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0144') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0144')) b where a.parentid = b.oid order by a.relname;

--test2: 分区名称-包含特殊字符
--step4: 创建二级分区表,分区名称包含特殊字符; expect:成功
drop table if exists t_subpartition_0144;
create  table if not exists t_subpartition_0144
(
  col_1 int ,
  col_2 int ,
    col_3 int ,
  col_4 int
)
tablespace ts_subpartition_0144
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
  subpartition "!!!"
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
--step5: 查看分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0144') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0144')) b where a.parentid = b.oid order by a.relname;
--step6: 插入数据; expect:成功
insert into t_subpartition_0144 values(21,49,1,1),(5,34,5,5),(8,188,8,8),(9,540,9,9),(19,9,9,9);
--step7: 查询分区名包含特殊字符的分区数据; expect:成功，1条数据
select * from t_subpartition_0144 subpartition("!!!");
--step8: 查询普通一级分区数据; expect:成功
select * from t_subpartition_0144 subpartition(p_hash_2_3);
--step9: 查询表数据; expect:成功
select * from t_subpartition_0144;
--step10: 插入数据; expect:成功
insert into t_subpartition_0144 values(49,49,1,1),(-5,34,5,5),(-8,188,8,8),(-9,540,9,9),(-1,9,9,9);
--step11: 查询普通一级分区数据; expect:成功，1条数据
select * from t_subpartition_0144 subpartition(p_hash_5_1);
--step12: 使用聚合函数查询二级分区数据; expect:成功
select max(col_4) from t_subpartition_0144 partition(p_list_5);
--step13: 查询二级分区的二级分区键数据; expect:成功
select col_2 from t_subpartition_0144 subpartition(p_hash_5_1);

--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0144;
drop tablespace if exists ts_subpartition_0144;
drop tablespace if exists ts_subpartition_0144_01;