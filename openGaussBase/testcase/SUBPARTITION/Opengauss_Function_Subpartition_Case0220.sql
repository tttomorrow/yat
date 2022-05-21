-- @testpoint: range_list二级分区表：with_query insert字段相同/字段数目不符,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0220;
drop tablespace if exists ts_subpartition_0220;
create tablespace ts_subpartition_0220 relative location 'subpartition_tablespace/subpartition_tablespace_0220';
drop tablespace if exists ts_subpartition_0220_01;
create tablespace ts_subpartition_0220_01 relative location 'subpartition_tablespace/subpartition_tablespace_0220_01';

--test1: insert --with_query  insert(字段相同)
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0220
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0220
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
--step3: 创建普通表; expect:成功
drop table if exists t_subpartition_0220_01;
create table if not exists t_subpartition_0220_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0220;
--step4: 插入数据; expect:成功
insert into t_subpartition_0220_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 查询临时表数据,查询到二级分区表; expect:成功
with with_t as (select 1,11,1,1) insert into t_subpartition_0220 (select * from with_t);
--step6: 查询普通表的数据,插入到二级分区表; expect:成功
insert into t_subpartition_0220 select * from t_subpartition_0220_01;
--step7: 二级分区表插入数据; expect:成功
insert into t_subpartition_0220 values(15,9,1,1);
--step8: 查询指定条件数据; expect:成功,2条数据
select * from t_subpartition_0220 partition(p_range_2) where col_4 > col_2/10;
 
--test2: insert --with_query  insert(字段数目不符)
--step9: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0220;
create table if not exists t_subpartition_0220
(
    col_1 int ,
    col_2 int ,
    col_3 int
)tablespace ts_subpartition_0220
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
--step10: 创建普通表; expect:成功
drop table if exists t_subpartition_0220_01;
create table if not exists t_subpartition_0220_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0220;
--step11: 普通表插入数据; expect:成功
insert into t_subpartition_0220_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step12: 查询临时表所有数据,插入到二级分区表; expect:合理报错
with with_t as (select 1,11,1,1) insert into t_subpartition_0220 (select * from with_t);
--step13: 查询普通表的所有数据,插入到二级分区表; expect:合理报错
insert into t_subpartition_0220 select * from t_subpartition_0220_01;
--step14: 查询普通表的指定2列数据,插入到二级分区表; expect:成功
insert into t_subpartition_0220 select col_1,col_2 from t_subpartition_0220_01;
--step15: 查询普通表的指定3列数据,插入到二级分区表; expect:成功
insert into t_subpartition_0220 select col_1,col_2,col_3 from t_subpartition_0220_01;
--step16: 查询数据; expect:成功
select * from t_subpartition_0220 partition(p_range_2) where col_3 is null;
--step17: 自联结count指定条件查询数据; expect:成功
select aa.col_1,count(aa.col_3)  from t_subpartition_0220 partition(p_range_2) aa,t_subpartition_0220 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2 /10 >5 group by aa.col_1;
--step18: 自联结sum指定条件查询数据; expect:成功
select aa.col_1,sum(aa.col_3)  from t_subpartition_0220 partition(p_range_2) aa,t_subpartition_0220 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2/10 >5 group by aa.col_1;
--step19: 自联结sum指定不同条件查询数据; expect:成功
select aa.col_1,sum(aa.col_3)  from t_subpartition_0220 partition(p_range_2) aa,t_subpartition_0220 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2/10 >5 and aa.col_3 is not null group by aa.col_1;
--step20: 自联结指定条件查询数据; expect:成功
select *  from t_subpartition_0220 partition(p_range_2) aa,t_subpartition_0220 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_2 /10 >5 and aa.col_3 is not null ;
--step21: 插入数据; expect:成功
insert into t_subpartition_0220 values(15,9,1);
--step22: 自联结min指定条件数据; expect:成功
select aa.col_1,min(bb.col_2)  from t_subpartition_0220 partition(p_range_2) aa,t_subpartition_0220 partition(p_range_2) bb  where aa.col_1=bb.col_3 and aa.col_3 is not null group by aa.col_1;
--step23: 查询指定数据,插入到二级分区表; expect:成功
insert into t_subpartition_0220 select col_1,to_char(col_2),col_3 from t_subpartition_0220_01;
insert into t_subpartition_0220 select col_1,to_char(sysdate,'YYYYMMDDHH'), (select col_1 from t_subpartition_0220 where col_1>8) aaa from (select col_1,col_3 from t_subpartition_0220 where col_1>5);

--step24: 清理环境; expect:成功
drop table if exists t_subpartition_0220;
drop table if exists t_subpartition_0220_01;
drop tablespace if exists ts_subpartition_0220;