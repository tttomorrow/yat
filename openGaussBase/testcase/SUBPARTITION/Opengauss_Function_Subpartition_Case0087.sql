-- @testpoint: list_range二级分区表：分区名称为普通字符串/特殊字符串,部分测试点合理报错

--test1: 分区名称-普通字符串
--step1: 创建二级分区表,分区名称为普通字符串; expect:成功
drop table if exists t_subpartition_0087;
drop tablespace if exists ts_subpartition_0087;
drop tablespace if exists ts_subpartition_0087_01;
create tablespace ts_subpartition_0087 relative location 'subpartition_tablespace/subpartition_tablespace_0087';
create tablespace ts_subpartition_0087_01 relative location 'subpartition_tablespace/subpartition_tablespace_0087_01';
create   table if not exists t_subpartition_0087
(
    col_1 int primary key   using index tablespace ts_subpartition_0087_01,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0087
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step2: 查询分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t
where p.reltablespace=t.oid and p.relname='p_list_4';
--step3: 查看分区信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0087') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0087')) b where a.parentid = b.oid order by a.relname;

--test2: 分区名称-包含特殊字符
--step4: 创建二级分区表,分区名称包含特殊字符; expect:成功
drop table if exists t_subpartition_0087;
drop tablespace if exists ts_subpartition_0087;
create tablespace ts_subpartition_0087 relative location 'subpartition_tablespace/subpartition_tablespace_0087';
create   table if not exists t_subpartition_0087
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0087
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition "!!!!!!!!!!!!!!" values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step5: 查看分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0087') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0087')) b where a.parentid = b.oid order by a.relname;
--step6: 插入数据; expect:成功
insert into t_subpartition_0087 values(-1,22,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9),(19,9,9,9);
--step7: 查询分区名包含特殊字符的分区数据; expect:成功，1条数据
select * from t_subpartition_0087 subpartition("!!!!!!!!!!!!!!");
--step8: 查询普通一级分区数据; expect:成功，1条数据
select * from t_subpartition_0087 partition(p_list_1);
--step9: 查询普通二级分区数据数据; expect:成功，3条数据
select * from t_subpartition_0087 subpartition(p_list_2_subpartdefault1);
--step10: 查询不存在的二级分区的数据; expect:合理报错
select * from t_subpartition_0087 subpartition(p_range_2_2);
--step11: 查询不存在的一级分区的数据; expect:合理报错
select max(col_4) from t_subpartition_0087 partition(p_range_2_subpartdefault1);
--step12: 使用聚合函数查询二级分区数据; expect:成功
select count(*) from t_subpartition_0087 subpartition(p_list_2_subpartdefault1);
--step13: 查询二级分区的二级分区键数据; expect:成功
select col_2 from t_subpartition_0087 subpartition(p_list_2_subpartdefault1);

--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0087;
drop tablespace if exists ts_subpartition_0087;
drop tablespace if exists ts_subpartition_0087_01;