-- @testpoint: range_hash二级分区表：表空间/分区名称为普通字符串/特殊字符串,部分测试点合理报错

--test1: tablespace
--step1: 创建二级分区表,指定表空间,一级分区主键using index tablespace; expect:成功
drop table if exists t_subpartition_0317;
drop tablespace if exists ts_subpartition_0317;
create tablespace ts_subpartition_0317 relative location 'subpartition_tablespace/subpartition_tablespace_0317';
drop tablespace if exists ts_subpartition_0317_01;
create tablespace ts_subpartition_0317_01 relative location 'subpartition_tablespace/subpartition_tablespace_0317_01';
create table if not exists t_subpartition_0317
(
    col_1 int primary key   using index tablespace ts_subpartition_0317_01,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0317
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
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step2: 查询指定一级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_2';
--step3: 查询指定一级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_1';
--step4: 查询指定二级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_5_subpartdefault1';

--test2: 分区名称-普通字符串
--step5: 创建二级分区表,分区名称为普通字符串; expect:成功
drop table if exists t_subpartition_0317;
create table if not exists t_subpartition_0317
(
    col_1 int primary key   using index tablespace ts_subpartition_0317_01,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0317
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
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step6: 查询分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_4';
--step7: 查看分区信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0317') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0317')) b where a.parentid = b.oid order by a.relname;

--test3: 分区名称-包含特殊字符
--step8: 创建二级分区表,分区名称包含特殊字符; expect:成功
drop table if exists t_subpartition_0317;
create table if not exists t_subpartition_0317
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0317
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
    subpartition "''"
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step9: 查看分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0317') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0317')) b where a.parentid = b.oid order by a.relname;
--step10: 插入数据; expect:成功
insert into t_subpartition_0317 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(49,9,9,9);
--step11: 查询分区名包含特殊字符的分区数据; expect:成功
select * from t_subpartition_0317 subpartition("''");
--step12: 查询普通一级分区数据; expect:成功
select * from t_subpartition_0317 partition(p_range_4);
--step13: 查询普通二级分区数据; expect:成功
select * from t_subpartition_0317 subpartition(p_range_2_subpartdefault1);
--step14: 查询不存在二级分区数据; expect:合理报错
select * from t_subpartition_0317 subpartition(p_range_1_2);
--step15: 查询不存在一级分区数据; expect:合理报错
select max(col_4) from t_subpartition_0317 partition(p_range_2_subpartdefault1);
--step16: 使用count查询二级分区数据; expect:成功
select count(*) from t_subpartition_0317 subpartition(p_range_2_subpartdefault1);
--step17: 查询二级分区数据的分区列; expect:成功
select col_2 from t_subpartition_0317 subpartition(p_range_2_subpartdefault1);

--step18: 清理环境; expect:成功
drop table if exists t_subpartition_0317;
drop tablespace if exists ts_subpartition_0317;
drop tablespace if exists ts_subpartition_0317_01;