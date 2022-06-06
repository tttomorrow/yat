-- @testpoint: list_hash二级分区表：相关系统表pg_partition/非分区列序列,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0169;
drop tablespace if exists ts_subpartition_0169;
create tablespace ts_subpartition_0169 relative location 'subpartition_tablespace/subpartition_tablespace_0169';

--test1: 相关系统表 --pg_partition
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0169
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0169
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
insert into t_subpartition_0169 values(-1,1,1,1),(-4,1,4,4),(-5,5,5,5),(-8,8,8,8),(-19,9,9,9);
insert into t_subpartition_0169 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0169 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step4: 查询系统表pg_partition数据; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0169') order by relname;
--step5: 查询指定系统表pg_partition数据; expect:成功
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0169')) b where a.parentid = b.oid order by a.relname;
--step6: 分区键创建唯一索引; expect:成功
drop index if exists index_01;
create unique index index_01 on t_subpartition_0169(col_1,col_2);
--step7: 设置分区索引不可用 expect:成功
alter index  index_01 modify partition p_list_3_subpartdefault1_col_1_col_2_idx  unusable;
--step8: 查看系统表分区索引; expect:成功,有数据
select relname, parttype, partstrategy, indisusable from pg_partition where relname = 'p_hash_2_3_col_1_col_2_idx';

--step9: 重命名分区索引 expect:成功
alter index index_01 rename partition p_list_3_subpartdefault1_col_1_col_2_idx to  aaaaaaa;
--step10: 设置分区索引不可用 expect:成功
alter index  index_01 modify partition aaaaaaa  unusable;
--step11: 重置分区索引可用 expect:成功
alter index index_01 rebuild  partition aaaaaaa ;
--step12: 设置分区内索引不可用 expect:合理报错
alter table t_subpartition_0169 modify partition p_hash_2  unusable local indexes;

--test2: 序列-非分区列序列
--step13: 创建二级分区表,声明非分区键的类型为序列整型; expect:成功
drop table if exists t_subpartition_0169;
create table if not exists t_subpartition_0169
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 serial
)tablespace ts_subpartition_0169
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
--step14: 插入数据; expect:成功
insert into t_subpartition_0169 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step15: 查询表数据; expect:成功,有数据
select * from t_subpartition_0169;
--step16: 清空表数据; expect:成功
truncate t_subpartition_0169;
--step17: 查询表数据; expect:成功,无数据
select * from t_subpartition_0169;

--step18: 插入数据; expect:成功
insert into t_subpartition_0169 values(81,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step19: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0169 subpartition(p_hash_5_1);
--step20: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0169 truncate subpartition p_hash_5_1;
--step21: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0169 subpartition(p_hash_5_1);

--step22: 插入数据; expect:成功
insert into t_subpartition_0169 values(11,1,1),(1,1,4),(15,5,5),(81,8,8),(19,9,9);
insert into t_subpartition_0169 values(18,1,1),(48,1,4),(57,5,5),(87,8,8),(95,9,9);
--step23: 查询表数据; expect:成功,有数据
select * from t_subpartition_0169;
--step24: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0169 subpartition(p_hash_2_2);
--step25: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0169 subpartition(p_hash_5_1);

--step26: 清理环境; expect:成功
drop table if exists t_subpartition_0169;
drop tablespace if exists ts_subpartition_0169;