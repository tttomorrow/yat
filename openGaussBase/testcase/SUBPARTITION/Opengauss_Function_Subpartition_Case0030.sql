-- @testpoint: list_list二级分区表：分区名称为数字开头/特殊字符串,部分测试点合理报错

--test1: 分区名称-数字开头
--step1: 创建二级分区表,分区名称为数字开头; expect:合理报错
drop table if exists t_subpartition_0030;
drop tablespace if exists ts_subpartition_0030;
create tablespace ts_subpartition_0030 relative location 'subpartition_tablespace/subpartition_tablespace_0030';
create   table if not exists t_subpartition_0030
(
    col_1 int ,
    col_2 int ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0030
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
	subpartition 11_o values ( 30,31,32,33,34,35,36,37,38,39 )
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

--step2: 创建二级分区表,分区名称为字符串，字符串中由数字开头; expect:成功
drop table if exists t_subpartition_0030;
drop tablespace if exists ts_subpartition_0030;
create tablespace ts_subpartition_0030 relative location 'subpartition_tablespace/subpartition_tablespace_0030';
create   table if not exists t_subpartition_0030
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0030
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
	subpartition "11_o" values ( 30,31,32,33,34,35,36,37,38,39 )
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
insert into t_subpartition_0030 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,39,9,9);
insert into t_subpartition_0030 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0030 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0030 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0030 values(-8,18,1);
--step4: 查询分区情况; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0030') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0030')) b where a.parentid = b.oid order by a.relname;
--step5: 查询数字开头的字符串的二级分区数据; expect:成功
select * from t_subpartition_0030 subpartition("11_o");
--step6: 查询普通二级分区数据数据; expect:成功
select * from t_subpartition_0030 subpartition(p_list_5_1);
--step7: 使用聚合函数查询普通一级分区数据数据; expect:成功
select max(col_4) from t_subpartition_0030 partition(p_list_2);
--step8: 查询二级分区的二级分区键数据; expect:成功
select col_2 from t_subpartition_0030 subpartition(p_list_3_2);
--step9: 二级分区键创建本地索引; expect:成功
drop index if exists i_subpartition_0030;
create index on t_subpartition_0030(col_2) local;

--step10: 清理环境; expect:成功
drop index if exists i_subpartition_0030;
drop table if exists t_subpartition_0030;
drop tablespace if exists ts_subpartition_0030;