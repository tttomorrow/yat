-- @testpoint: list_hash二级分区表：分区名称为数据库关键字，部分测试点合理报错

--test1: 分区名称-数据库关键字命名
--step1: 创建二级分区表,二级分区名称为数据库关键字命名; expect:成功
drop table if exists t_subpartition_0146;
drop tablespace if exists ts_subpartition_0146;
create tablespace ts_subpartition_0146 relative location 'subpartition_tablespace/subpartition_tablespace_0146';
create table if not exists t_subpartition_0146
(
  col_1 int ,
  col_2 int ,
    col_3 int ,
  col_4 int
)
tablespace ts_subpartition_0146
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
  subpartition index
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
--step2: 插入数据; expect:成功
insert into t_subpartition_0146 values(25,88,1);
--step3: 查询关键字命名的二级分区数据; expect:成功，1条数据
select * from t_subpartition_0146 subpartition(index);
--step4: 更新关键字命名的二级分区数据; expect:成功
update t_subpartition_0146 set col_1=36 where col_1=25;
--step5: 查询关键字命名的二级分区数据; expect:成功，0条数据
select * from t_subpartition_0146 subpartition(index);
--step6: 更新关闭行移动; expect:成功
alter table t_subpartition_0146 disable row movement;
--step7: 插入数据; expect:成功
insert into t_subpartition_0146 values(25,88,1);
--step8: 查询关键字命名的二级分区数据; expect:成功，1条数据
select * from t_subpartition_0146 subpartition(index);
--step9: 更新清空关键字命名的二级分区数据; expect:成功
alter table t_subpartition_0146 truncate subpartition index;
--step10: 查询关键字命名的二级分区数据; expect:成功，0条数据
select * from t_subpartition_0146 subpartition(index);
--step11: 查询数据; expect:成功
select * from t_subpartition_0146;

--step12: 创建二级分区表,二级分区名称为表名; expect:成功
drop table if exists t_subpartition_0146;
create  table if not exists t_subpartition_0146
(
  col_1 int ,
  col_2 int ,
    col_3 int ,
  col_4 int
)
tablespace ts_subpartition_0146
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
  subpartition t_subpartition_0146
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
) disable row movement ;
--step13: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0146') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0146')) b where a.parentid = b.oid order by a.relname;
--step14: 插入数据; expect:成功
insert into t_subpartition_0146 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0146 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,29,9,9);
insert into t_subpartition_0146 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0146 values(38,38,7,7);
--step15: 查询表名命名的二级分区数据; expect:成功
select * from t_subpartition_0146 subpartition(t_subpartition_0146);
--step16: 查询指定一级分区数据; expect:成功
select * from t_subpartition_0146 partition(p_list_4);
--step17: 删除指定数据; expect:成功
delete t_subpartition_0146 where col_1 =18 or col_1 =15;
--step18: 分区键创建唯一索引; expect:成功
create unique index on t_subpartition_0146(col_1,col_2);
--step19: 查询数据; expect:成功
select * from t_subpartition_0146;
--step20: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0146') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0146')) b where a.parentid = b.oid order by a.relname;

--step21: 清理环境; expect:成功
drop table if exists t_subpartition_0146;
drop tablespace if exists ts_subpartition_0146;
