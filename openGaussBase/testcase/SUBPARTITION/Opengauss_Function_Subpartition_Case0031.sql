-- @testpoint: list_list二级分区表：分区名称为数据库关键字/列名命名

--test1: 分区名称-数据库关键字命名
--step1: 创建二级分区表,二级分区名称为数据库关键字命名; expect:成功
drop table if exists t_subpartition_0031;
drop tablespace if exists ts_subpartition_0031;
create tablespace ts_subpartition_0031 relative location 'subpartition_tablespace/subpartition_tablespace_0031';
create table if not exists t_subpartition_0031
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0031
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
    subpartition index values ( 30,31,32,33,34,35,36,37,38,39 )
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
--step2: 插入数据; expect:成功
insert into t_subpartition_0031 values(8,38,1);
--step3: 查询关键字命名的二级区分数据; expect:成功
select * from t_subpartition_0031 subpartition(index);
--step4: 更新关键字命名的二级区分数据; expect:成功
update t_subpartition_0031 set col_2=36 where col_1=8;
--step5: 查询关键字命名的二级区分数据; expect:成功
select * from t_subpartition_0031 subpartition(index);
--step6: 清空关键字命名的二级区分数据; expect:成功
alter table t_subpartition_0031 truncate subpartition  index;
--step7: 查询关键字命名的二级区分数据; expect:成功，0条数据
select * from t_subpartition_0031 subpartition(index);
 --step8: 查询全部数据; expect:成功
select * from t_subpartition_0031;

--test2: 分区名称-列名命名
--step9: 创建二级分区表,二级分区名称为列名; expect:成功
drop table if exists t_subpartition_0031;
create table if not exists t_subpartition_0031
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0031
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
    subpartition col_4 values ( 30,31,32,33,34,35,36,37,38,39 )
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
--step10: 查询分区信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0031') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0031')) b where a.parentid = b.oid order by a.relname;
--step11: 插入数据; expect:成功
insert into t_subpartition_0031 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0031 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0031 values(21,11,1,1),(-29,31,9,9),(8,38,7,7);
--step12: 查询一级分区数据; expect:成功
select * from t_subpartition_0031 partition(p_list_2);
--step13: 查询二级分区数据; expect:成功
select * from t_subpartition_0031 subpartition(col_4);
--step14: 分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0031;
create unique index i_subpartition_0031 on t_subpartition_0031(col_1,col_2);
--step15: 查询分区索引信息; expect:成功
select relname, parttype, partstrategy, indisusable from pg_partition where relname = 'col_4_col_1_col_2_idx';
select relname, parttype, partstrategy, indisusable from pg_partition where relname = 'p_list_1_2_col_1_col_2_idx';


--step16: 删除表; expect:成功
drop index if exists i_subpartition_0031;
drop table if exists t_subpartition_0031;
drop tablespace if exists ts_subpartition_0031;