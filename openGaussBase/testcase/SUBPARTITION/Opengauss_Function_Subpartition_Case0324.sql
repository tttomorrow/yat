-- @testpoint: range_hash二级分区表：分区数0/1,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0324;
drop tablespace if exists ts_subpartition_0324;
create tablespace ts_subpartition_0324 relative location 'subpartition_tablespace/subpartition_tablespace_0324';

--test1: 分区数--0个
--step2: 创建二级分区表,一级和二级分区数为0; expect:合理报错
create   table if not exists t_subpartition_0324
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0324
partition by range (col_1) subpartition by hash (col_2)
(
) enable row movement;
--step3: 创建二级分区表,二级分区数为0; expect:成功
drop table if exists t_subpartition_0324;
create   table if not exists t_subpartition_0324
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0324
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30),
  partition p_range_4 values less than( 50),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step4: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0324') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0324')) b where a.parentid = b.oid order by a.relname;

--test2: 分区数--1个
--step5: 创建二级分区表,二级分区数为1; expect:成功
drop table if exists t_subpartition_0324;
create   table if not exists t_subpartition_0324
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0324
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 
  )
) enable row movement; 
--step6: 插入数据; expect:成功
insert into t_subpartition_0324 values(-21,1,1,1),(-25,5,5,5),(-28,8,8,8),(-29,9,9,9);

--step7: 创建二级分区表,二级分区数0; expect:成功
drop table if exists t_subpartition_0324;
create   table if not exists t_subpartition_0324
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0324
partition by range (col_1) subpartition by hash (col_2) (
 partition p_range_1 values less than( -10 )
) enable row movement;
--step8: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0324') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0324')) b where a.parentid = b.oid order by a.relname;
--step9: 插入数据; expect:成功
insert into t_subpartition_0324 values(-21,1,1,1),(-25,5,5,5),(-28,8,8,8),(-29,9,9,9);
--step10: 查询指定一级分区数据; expect:成功
select * from t_subpartition_0324 partition(p_range_1);
--step11: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0324 subpartition(p_range_1_subpartdefault1);

--step12: 清理环境; expect:成功
drop table if exists t_subpartition_0324;
drop tablespace if exists ts_subpartition_0324;
