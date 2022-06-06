-- @testpoint: list_list二级分区表：相关系统表pg_partition/非分区列序列,部分测试点合理报错

--test1: 相关系统表 --pg_partition
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0054;
drop tablespace if exists ts_subpartition_0054;
create tablespace ts_subpartition_0054 relative location 'subpartition_tablespace/subpartition_tablespace_0054';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0054
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0054
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
    subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
    subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0054 values(-1,1,1,1),(-4,1,4,4),(-5,5,5,5),(-8,8,8,8),(-19,9,9,9);
--step4: 插入数据; expect:成功
insert into t_subpartition_0054 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0054 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step5: 查询指定系统表pg_partition数据; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0054') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0054')) b where a.parentid = b.oid order by a.relname;
--step6: 分区键创建唯一索引; expect:成功
drop index if exists index_01;
create unique index index_01 on t_subpartition_0054(col_1,col_2);
--step7: 设置分区索引不可用 expect:成功
alter index  index_01 modify partition p_list_3_2_col_1_col_2_idx  unusable;
--step8: 查看系统表分区索引; expect:成功，有数据
select relname, parttype, partstrategy, indisusable from pg_partition where relname = 'p_list_1_1_col_1_col_2_idx';

--step9: 重命名分区索引 expect:成功
alter index index_01 rename partition p_list_5_2_col_1_col_2_idx to  aaaaaaa;
--step10: 设置分区索引不可用 expect:成功
alter index  index_01 modify partition aaaaaaa  unusable;
--step11: 重置分区索引可用 expect:成功
alter index index_01 rebuild  partition aaaaaaa ;
--step12: 设置分区内索引不可用 expect:合理报错
alter table t_subpartition_0054 modify partition p_list_2  unusable local indexes;

--test2: 序列-非分区列序列
--step13: 创建二级分区表，声明非分区键的类型为序列整型; expect:成功
drop table if exists t_subpartition_0054;
create table if not exists t_subpartition_0054
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 serial
)tablespace ts_subpartition_0054
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
    subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
    subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
    subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
    subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step14: 插入数据; expect:成功
insert into t_subpartition_0054 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step15: 查询表数据; expect:成功，有数据
select * from t_subpartition_0054;
--step16: 清空表数据; expect:成功
truncate t_subpartition_0054;
--step17: 查询表数据; expect:成功，无数据
select * from t_subpartition_0054;

--step18: 插入数据; expect:成功
insert into t_subpartition_0054 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step19: 查询指定二级分区数据; expect:成功，有数据
select * from t_subpartition_0054 subpartition(p_list_2_1);
--step20: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0054 truncate subpartition p_list_2_1;
--step21: 查询指定二级分区数据; expect:成功，无数据
select * from t_subpartition_0054 subpartition(p_list_2_1);

--step22: 插入数据; expect:成功
insert into t_subpartition_0054 values(11,1,1),(1,1,4),(15,5,5),(81,8,8),(19,9,9);
insert into t_subpartition_0054 values(18,1,1),(48,1,4),(57,5,5),(87,8,8),(95,9,9);
--step23: 查询表数据; expect:成功，有数据
select * from t_subpartition_0054;
--step24: 查询指定二级分区数据; expect:成功，有数据
select * from t_subpartition_0054 subpartition(p_list_2_1);
--step25: 查询指定二级分区数据; expect:成功，有数据
select * from t_subpartition_0054 subpartition(p_list_3_2);

--step26: 删除表; expect:成功
drop table if exists t_subpartition_0054;
drop tablespace if exists ts_subpartition_0054;