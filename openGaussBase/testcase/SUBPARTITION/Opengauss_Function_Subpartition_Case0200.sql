-- @testpoint: range_list二级分区表：表空间

--test1: tablespace
--step1: 创建二级分区表，指定表空间，一级分区主键using index tablespace; expect:成功
drop table if exists t_subpartition_0200;
drop tablespace if exists ts_subpartition_0200;
create tablespace ts_subpartition_0200 relative location 'subpartition_tablespace/subpartition_tablespace_0200';
drop tablespace if exists ts_subpartition_0200_01;
create tablespace ts_subpartition_0200_01 relative location 'subpartition_tablespace/subpartition_tablespace_0200_01';
create   table if not exists t_subpartition_0200
(
    col_1 int primary key   using index tablespace ts_subpartition_0200_01,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0200
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
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
--step2: 查询指定一级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_2';
--step3: 查询指定一级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_1';
--step4: 查询指定二级分区表空间; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_5_subpartdefault1';

--step6: 创建二级分区表，指定表空间; expect:成功
drop table if exists t_subpartition_0200;
create   table if not exists t_subpartition_0200
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0200
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
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
--step7: 在不同的空间为分区键创建唯一索引; expect:成功
create unique index on t_subpartition_0200( col_1,col_2) tablespace ts_subpartition_0200_01;
--step8: 查看分区tablespace; expect:成功
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_5_subpartdefault1';
--step9: 查询分区索引p_range_5_subpartdefault1_col_1_col_2_idx的tablespace; expect:成功，和分区空间不同
select p.relname, t.spcname from pg_partition p, pg_tablespace t where p.reltablespace=t.oid and p.relname='p_range_5_subpartdefault1_col_1_col_2_idx';

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0200;
drop tablespace if exists ts_subpartition_0200;