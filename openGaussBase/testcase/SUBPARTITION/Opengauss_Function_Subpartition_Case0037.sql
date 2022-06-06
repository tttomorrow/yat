-- @testpoint: list_list二级分区表：分区数1个/分区键非顺序指定,部分测试点合理报错

--test1: 分区数1个
--step1: 创建二级分区表,一级分区数和二级分区数各1个; expect:成功
drop table if exists t_subpartition_0037;
drop tablespace if exists ts_subpartition_0037;
create tablespace ts_subpartition_0037 relative location 'subpartition_tablespace/subpartition_tablespace_0037';
create table if not exists t_subpartition_0037
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0037
partition by list (col_1) subpartition by list (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values( -10 )
)
) enable row movement;
--step2: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable ,boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0037') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0037')) b where a.parentid = b.oid order by a.relname;

--step3: 插入数据; expect:成功
insert into t_subpartition_0037 values(-8,-10,1);
--step4: 查询数据; expect:成功
select * from t_subpartition_0037;
--step5: 查询二级分区数据; expect:成功
select * from t_subpartition_0037 subpartition (p_list_1_1);

--step6: 创建二级分区表,一级分区数1个，二级分区数0; expect:成功
drop table if exists t_subpartition_0037;
drop tablespace if exists ts_subpartition_0037;
create tablespace ts_subpartition_0037 relative location 'subpartition_tablespace/subpartition_tablespace_0037';
create table if not exists t_subpartition_0037
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0037
partition by list (col_1) subpartition by list (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 ) enable row movement;
--step7: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0037') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0037')) b where a.parentid = b.oid order by a.relname;
--step8: 插入数据; expect:成功
insert into t_subpartition_0037 values(-1,-1,-1,1),(-5,5,5,5),(-8,8,8,8),(-9,9,9,9);
--step8: 插入不在分区范围内的数据; expect:合理报错
insert into t_subpartition_0037 values(11,1,1,1),(15,5,5,5),(18,8,8,8),(19,9,9,9);
--step8: 插入不在分区范围内的数据; expect:合理报错
insert into t_subpartition_0037 values(-21,1,1,1),(-25,5,5,5),(-28,8,8,8),(-29,9,9,9);
--step9: 查询一级分区数据; expect:成功
select * from t_subpartition_0037 partition(p_list_1);
--step10: 查询二级分区default数据; expect:成功
select * from t_subpartition_0037 subpartition(p_list_1_subpartdefault1);

--test2: 分区键--非顺序指定
--step11: 创建二级分区表,一级分区键非顺序指定; expect:成功
drop table if exists t_subpartition_0037;
create table if not exists t_subpartition_0037
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int ,
    col_19 int
)
tablespace ts_subpartition_0037
partition by list (col_19) subpartition by list (col_2)
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
--step12: 创建二级分区表,一级分区键和二级分区键非顺序指定; expect:成功
drop table if exists t_subpartition_0037;
create table t_subpartition_0037
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by list (col_2) subpartition by list (col_1)
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
--step13: 插入数据(反向分区); expect:成功
insert into t_subpartition_0037 values(-1,1,1,1);
--step14: 查询二级分区数据; expect:成功，0条数据
select *  from t_subpartition_0037 subpartition(p_list_1_2);
--step15: 查询二级分区数据; expect:成功，1条数据
select *  from t_subpartition_0037 subpartition(p_list_2_2);

--step16: 删除表; expect:成功
drop table if exists t_subpartition_0037;
drop tablespace if exists ts_subpartition_0037;