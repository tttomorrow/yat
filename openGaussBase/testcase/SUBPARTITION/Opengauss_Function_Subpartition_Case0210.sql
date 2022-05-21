-- @testpoint: range_list二级分区表：分区数1个/less than表达式/start—end,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0210;
drop tablespace if exists ts_subpartition_0210;
create tablespace ts_subpartition_0210 relative location 'subpartition_tablespace/subpartition_tablespace_0210';

--test1: 分区数--1个
--step2: 创建二级分区表,一级分区数和二级分区数各1个; expect:成功
create   table if not exists t_subpartition_0210
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0210
partition by range (col_1) subpartition by list ( col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5')
  )
) enable row movement;

--step3: 创建二级分区表,一级分区中二级分区数0; expect:成功
drop table if exists t_subpartition_0210;
create   table if not exists t_subpartition_0210
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0210
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step4: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0210') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0210')) b where a.parentid = b.oid order by a.relname;
--step5: 插入数据; expect:成功
insert into t_subpartition_0210 values(-1,-1,-1,1),(-5,5,5,5),(-8,8,8,8),(-9,9,9,9);
insert into t_subpartition_0210 values(11,1,1,1),(15,5,5,5),(18,8,8,8),(19,9,9,9);
insert into t_subpartition_0210 values(21,1,1,1),(25,5,5,5),(28,8,8,8),(29,9,9,9);
--step6: 查询一级分区数据; expect:成功
select * from t_subpartition_0210 partition(p_range_2);
--step7: 查询二级分区default数据; expect:成功
select * from t_subpartition_0210 subpartition(p_list_3_1);

--test2: start end语法
--step8: 创建二级分区表,分区键范围指定start end; expect:合理报错
drop table if exists t_subpartition_0210;
create table t_subpartition_0210 (c1 int , c2 int primary key ,c3 int )
partition by range (c1) subpartition by range ( c2)
(
partition p1 start(1) end(1000) 
  (
    subpartition p_list_1_1 values less than( 5 )
  ))enable row movement;

--test3: less than  (表达式)
--step9: 创建二级分区表,分区键类型和范围不符; expect:成功
drop table if exists t_subpartition_0210;
create   table if not exists t_subpartition_0210
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int ,
	col_19 timestamp with time zone
)
tablespace ts_subpartition_0210
partition by range (col_19) subpartition by list (col_2)
(
  partition p_range_1 values less than( to_date('2022-11-01','yyyy-mm-dd') )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than(to_date('2023-11-01','yyyy-mm-dd'))
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( to_date('2024-11-01','yyyy-mm-dd') )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( to_date('2025-11-01','yyyy-mm-dd'))
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step10: 创建二级分区表,分区键类型和范围相符; expect:成功
drop table if exists t_subpartition_0210;
create   table if not exists t_subpartition_0210
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int ,
	col_19 timestamp with time zone	
)
tablespace ts_subpartition_0210
partition by range (col_19) subpartition by list (col_2)
(
  partition p_range_1 values less than( to_date('2022-11-01','yyyy-mm-dd') )
  (
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than(to_date('2023-11-01','yyyy-mm-dd'))
  (
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( to_date('2024-11-01','yyyy-mm-dd') )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( to_date('2025-11-01','yyyy-mm-dd'))
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--step11: 清理环境; expect:成功
drop table if exists t_subpartition_0210;
drop tablespace if exists ts_subpartition_0210;