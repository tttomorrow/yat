-- @testpoint: range_hash二级分区表：分区键非顺序指定/less than表达式/start—end,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0325;
drop tablespace if exists ts_subpartition_0325;
create tablespace ts_subpartition_0325 relative location 'subpartition_tablespace/subpartition_tablespace_0325';

--test1: 分区键--非顺序指定
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0325
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int ,
	col_19 int
)
tablespace ts_subpartition_0325
partition by range (col_19) subpartition by hash (col_2)
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
	subpartition t_subpartition_0325
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--test2: start end语法
--step3: 创建二级分区表,分区键范围指定start end; expect:合理报错
drop table if exists t_subpartition_0325;
create table partition_range_01 (c1 int , c2 int primary key ,c3 int )
partition by range (c1) subpartition by range ( c2)
(
partition p1 start(1) end(1000) 
  (
    subpartition p_list_1_1 values less than( 5 )
  ))enable row movement;

--test3:  less than  (表达式)
--step4: 创建二级分区表,分区less than  (表达式); expect:成功
drop table if exists t_subpartition_0325;
create   table if not exists t_subpartition_0325
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int ,
	col_19 timestamp with time zone	,
	col_20 int 
)
tablespace ts_subpartition_0325
partition by range (col_19) subpartition by hash (col_20)
(
  partition p_range_1 values less than( to_date('2018-11-01','yyyy-mm-dd' ))
  (
    subpartition p_hash_1_1
  ),
  partition p_range_2 values less than( to_date('2018-12-01','yyyy-mm-dd' )),
  partition p_range_3 values less than( to_date('2019-11-01','yyyy-mm-dd'))
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
	subpartition p_hash_3_3
  ),
    partition p_range_4 values less than(to_date( '2020-11-01','yyyy-mm-dd'))
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
	subpartition t_subpartition_0325
  ),
  partition p_range_5 values less than( to_date('2021-11-01','yyyy-mm-dd'))
) enable row movement;
--step5: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0325') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0325')) b where a.parentid = b.oid order by a.relname;
--step6: 插入数据; expect:成功
insert into t_subpartition_0325 values(1,1,1,1,'2018-05-08',1);
--step7: 查询数据; expect:成功
select * from t_subpartition_0325 partition(p_range_1);
--step8: 查询数据; expect:成功
select * from t_subpartition_0325 subpartition(p_hash_1_1);

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0325;
drop tablespace if exists ts_subpartition_0325;