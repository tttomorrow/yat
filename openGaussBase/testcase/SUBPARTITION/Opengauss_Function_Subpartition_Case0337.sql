-- @testpoint: range_hash二级分区表：相关系统表pg_partition/非分区列序列,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0337;
drop tablespace if exists ts_subpartition_0337;
create tablespace ts_subpartition_0337 relative location 'subpartition_tablespace/subpartition_tablespace_0337';

--test1: 相关系统表 --pg_partition
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0337
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0337
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
    subpartition t_subpartition_0337
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0337 values(-1,1,1,1),(-4,1,4,4),(-5,5,5,5),(-8,8,8,8),(-19,9,9,9);
insert into t_subpartition_0337 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0337 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step4: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0337') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0337')) b where a.parentid = b.oid order by a.relname;
--step5: 分区键创建索引; expect:成功
drop index if exists t_subpartition_0337_col_2_idx;
create index t_subpartition_0337_col_2_idx on t_subpartition_0337(col_2) local ;
--step6: 系统表查看索引信息 expect:成功
select relname, parttype, partstrategy, boundaries, indisusable from pg_partition where relname = 'p_hash_1_2_col_2_idx';
--step7: 设置分区索引不可用 expect:成功
alter index  t_subpartition_0337_col_2_idx modify partition p_hash_1_2_col_2_idx  unusable;
--step8: 系统表查看索引信息 expect:成功,indisusable的值为f
select relname, parttype, partstrategy, boundaries, indisusable from pg_partition where relname = 'p_hash_1_2_col_2_idx';

--step9: 重命名分区索引 expect:成功
alter index t_subpartition_0337_col_2_idx rename partition p_hash_1_2_col_2_idx to  aaaaaaa;
--step10: 设置分区索引不可用 expect:成功
alter index  t_subpartition_0337_col_2_idx modify partition aaaaaaa  unusable;
--step11: 重置分区索引可用 expect:成功
alter index t_subpartition_0337_col_2_idx rebuild  partition aaaaaaa ;
--step12: 设置分区内索引不可用 expect:合理报错
alter table t_subpartition_0337 modify partition p_range_2  unusable local indexes;

--test2: 序列--非分区列序列,声明非分区键的类型为序列整型
--step13: 创建二级分区表,声明非分区键的类型为序列整型; expect:成功
create table if not exists t_subpartition_0337
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 serial
)tablespace ts_subpartition_0337
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
    subpartition t_subpartition_0337
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step14: 插入数据; expect:成功
insert into t_subpartition_0337 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step15: 查询表数据; expect:成功,有数据
select * from t_subpartition_0337;
--step16: 清空表数据; expect:成功
truncate t_subpartition_0337;
--step17: 查询表数据; expect:成功,无数据
select * from t_subpartition_0337;

--step18: 插入数据; expect:成功
insert into t_subpartition_0337 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step19: 查询数据; expect:成功,有数据
select * from t_subpartition_0337;
--step20: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0337 subpartition(p_range_2_subpartdefault1);
--step21: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0337 truncate subpartition p_range_2_subpartdefault1;
--step22: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0337 subpartition(p_range_2_subpartdefault1);

--step23: 插入数据; expect:成功
insert into t_subpartition_0337 values(11,1,1),(1,1,4),(15,5,5),(81,8,8),(19,9,9);
insert into t_subpartition_0337 values(18,1,1),(48,1,4),(57,5,5),(87,8,8),(95,9,9);
--step24: 查询数据; expect:成功,有数据
select * from t_subpartition_0337 subpartition(p_range_2_subpartdefault1);
--step25: 查询数据; expect:成功,有数据
select * from t_subpartition_0337 subpartition(p_range_5_subpartdefault1);

--test3: 序列--非分区列序列,指定序列与列的归属关系
--step26: 创建序列; expect:成功
drop sequence if exists seql_subpartition_0337;
create sequence seql_subpartition_0337 cache 100;
--step27: 创建二级分区表,将序列值作为非分区列的默认值,使该字段具有唯一标识属性; expect:成功
drop table if exists t_subpartition_0337;
create table if not exists t_subpartition_0337
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int not null default nextval('seql_subpartition_0337')
)tablespace ts_subpartition_0337
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
    subpartition t_subpartition_0337
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step28: 指定序列与列的归属关系; expect:成功
alter sequence seql_subpartition_0337 owned by t_subpartition_0337.col_4;
--step29: 插入数据; expect:成功
insert into t_subpartition_0337 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0337 values(11,1,1),(1,1,4),(15,5,5),(81,8,8),(19,9,9);
insert into t_subpartition_0337 values(18,1,1),(48,1,4),(57,5,5),(87,8,8),(95,9,9);

--step30: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0337 subpartition(p_range_2_subpartdefault1);
--step31: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0337 subpartition(p_range_5_subpartdefault1);
--step32: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0337 truncate subpartition p_range_5_subpartdefault1;
--step33: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0337 subpartition(p_range_5_subpartdefault1);
--step34: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0337 subpartition(p_range_2_subpartdefault1);
--step35: 插入数据; expect:成功
insert into t_subpartition_0337 values(81,1,1),(94,1,4),(445,5,5),(8768,8,8),(7869,9,9);
--step36: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0337 subpartition(p_range_5_subpartdefault1);
--step37: 查询表数据; expect:成功,有数据
select * from t_subpartition_0337;

--step38: 清理环境; expect:成功
drop table if exists t_subpartition_0337;
drop tablespace if exists ts_subpartition_0337;