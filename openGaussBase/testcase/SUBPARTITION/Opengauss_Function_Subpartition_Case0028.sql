-- @testpoint: list_list二级分区表：表空间

--test1: tablespace
--step1: 创建二级分区表，指定表空间，一级分区主键using index tablespace; expect:成功
drop table if exists t_subpartition_0028;
drop tablespace if exists ts_subpartition_0028;
create tablespace ts_subpartition_0028 relative location 'subpartition_tablespace/subpartition_tablespace_0028';
create   table if not exists t_subpartition_0028
(
    col_1 int primary key   using index tablespace ts_subpartition_0028,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0028
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
--step2: 查询表的表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='t_subpartition_0028' order by relname;

--step3: 创建二级分区表，指定表空间; expect:成功
drop table if exists t_subpartition_0028;
drop tablespace if exists ts_subpartition_0028;
create tablespace ts_subpartition_0028 relative location 'subpartition_tablespace/subpartition_tablespace_0028';
drop tablespace if exists ts_subpartition_0028_01;
create tablespace ts_subpartition_0028_01 relative location 'subpartition_tablespace/subpartition_tablespace_0028_01';
create table if not exists t_subpartition_0028
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0028
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
--step4: 分区键创建唯一性索引，指定表空间; expect:成功
create unique index on t_subpartition_0028( col_1,col_2)  tablespace ts_subpartition_0028_01;
--step5: 查询数据; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0028') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0028')) b where a.parentid = b.oid order by a.relname;
--step6: 查看二级分区tablespace; expect:成功,表空间为ts_subpartition_0028
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_list_5_5';
--step7: 查看一级分区tablespace; expect:成功,表空间为ts_subpartition_0028
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_list_6';
--step8: 查看表tablespace; expect:成功,表空间为ts_subpartition_0028
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='t_subpartition_0028';

--step9: 删除表; expect:成功
drop table if exists t_subpartition_0028;
drop tablespace if exists ts_subpartition_0028;
drop tablespace if exists ts_subpartition_0028_01;