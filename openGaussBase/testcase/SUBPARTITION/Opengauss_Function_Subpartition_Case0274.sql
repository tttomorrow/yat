-- @testpoint: range_range二级分区表：分区数0/1/less than表达式/start—end,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0274;
drop tablespace if exists ts_subpartition_0274;
create tablespace ts_subpartition_0274 relative location 'subpartition_tablespace/subpartition_tablespace_0274';

--test1: 分区数--0个
--step2: 创建二级分区表,二级分区数为0; expect:成功
create   table if not exists t_subpartition_0274
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0274
partition by range (col_1) subpartition by range ( col_2)
(
  partition p_range_1 values less than( 10 ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30 )
) enable row movement;
--step3: 查询数据; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0274') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0274')) b where a.parentid = b.oid order by a.relname;
--step4: 插入数据; expect:成功
insert into t_subpartition_0274 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0274 values(11,1,1,1),(15,5,5,5),(18,8,8,8),(19,9,9,9);
insert into t_subpartition_0274 values(21,1,1,1),(25,5,5,5),(28,8,8,8),(29,9,9,9);
--step5: 查询指定一级分区数据; expect:成功
select * from t_subpartition_0274 partition(p_range_1);
--step6: 查询默认二级分区数据; expect:成功
select * from t_subpartition_0274 subpartition(p_range_2_subpartdefault1);

--test2: 分区数--1个
--step7: 创建二级分区表,二级分区数为1; expect:成功
drop table if exists t_subpartition_0274;
create   table if not exists t_subpartition_0274
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0274
partition by range (col_1) subpartition by range ( col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 )
  )
) enable row movement;

--test3: start end语法
--step8: 创建二级分区表,分区键范围指定start end; expect:合理报错
drop table if exists t_subpartition_0274;
create table partition_range_01 (c1 int , c2 int primary key ,c3 int )
partition by range (c1) subpartition by range ( c2)
(
partition p1 start(1) end(1000) every(200)
  (
    subpartition p_range_1_1 values less than( 5 )
  ),
partition p2 end(2000),
partition p3 start(2000) end(2500) tablespace startend_tbs3,
partition p4 start(2500),
partition p5 start(3000) end(5000) every(1000) tablespace startend_tbs4
)enable row movement;

--test4:  less than  (表达式)
--step9: 创建二级分区表,分区less than  (表达式); expect:成功
drop table if exists t_subpartition_0274;
create   table if not exists t_subpartition_0274
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0274
partition by range (col_1 ) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( to_number(5+3)),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step10: 查询数据; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0274') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0274')) b where a.parentid = b.oid order by a.relname;
--step11: 插入数据; expect:成功
insert into t_subpartition_0274 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step12: 查询指定一级分区数据; expect:成功
select * from t_subpartition_0274 partition(p_range_1);
--step13: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0274 subpartition(p_range_1_1);

--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0274;
drop tablespace if exists ts_subpartition_0274;
