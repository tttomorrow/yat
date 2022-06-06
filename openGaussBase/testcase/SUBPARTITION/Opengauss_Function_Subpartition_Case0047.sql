-- @testpoint: list_list二级分区表：with_query insert字段相同/字段数目不符,部分测试点合理报错

--test1: insert --with_query  insert(字段相同)
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0047;
drop table if exists t_subpartition_0047_01;
drop tablespace if exists ts_subpartition_0047;
create tablespace ts_subpartition_0047 relative location 'subpartition_tablespace/subpartition_tablespace_0047';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0047
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0047
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
--step3: 创建普通表; expect:成功
drop table if exists t_subpartition_0047_01;
create table if not exists t_subpartition_0047_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0047;
--step4: 普通表插入数据; expect:成功
insert into t_subpartition_0047_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step5: 查询临时表数据，查询到二级分区表; expect:成功
with with_t as (select 1,11,1,1) insert into t_subpartition_0047 (select * from with_t);
--step6: 查询普通表的数据，插入到二级分区表; expect:成功
insert into t_subpartition_0047 select * from t_subpartition_0047_01;
--step7: 二级分区表插入数据; expect:成功
insert into t_subpartition_0047 values(15,9,1,1);
--step8: 查询指定条件数据; expect:成功，1条数据
select * from t_subpartition_0047 partition(p_list_2) where col_4 > col_2/10;

--test2: insert --with_query  insert(字段数目不符)
--step9: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0047;
create table if not exists t_subpartition_0047
(
    col_1 int ,
    col_2 int ,
    col_3 int
)tablespace ts_subpartition_0047
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
--step10: 创建普通表; expect:成功
drop table if exists t_subpartition_0047_01;
create table if not exists t_subpartition_0047_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0047;
--step11: 普通表插入数据; expect:成功
insert into t_subpartition_0047_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step12: 查询临时表所有数据，查询到二级分区表; expect:合理报错
with with_t as (select 1,11,1,1) insert into t_subpartition_0047 (select * from with_t);
--step13: 查询普通表的所有数据，插入到二级分区表; expect:合理报错
insert into t_subpartition_0047 select * from t_subpartition_0047_01;
--step14: 查询普通表的指定2列数据，插入到二级分区表; expect:成功
insert into t_subpartition_0047 select col_1,col_2 from t_subpartition_0047_01;
--step15: 查询普通表的指定3列数据，插入到二级分区表; expect:成功
insert into t_subpartition_0047 select col_1,col_2,col_3 from t_subpartition_0047_01;
--step16: 查询数据; expect:成功，5条数据
select * from t_subpartition_0047 partition(p_list_2) where col_3 is null;
--step17: 自联结count指定条件查询数据; expect:成功
select aa.col_1,count(aa.col_3)  from t_subpartition_0047 partition(p_list_2) aa,t_subpartition_0047 partition(p_list_2) bb  where aa.col_1=bb.col_3 and aa.col_2 /10 >5 group by aa.col_1;
--step18: 自联结sum指定条件查询数据; expect:成功
select aa.col_1,sum(aa.col_3)  from t_subpartition_0047 partition(p_list_2) aa,t_subpartition_0047 partition(p_list_2) bb  where aa.col_1=bb.col_3 and aa.col_2/10 >5 group by aa.col_1;
--step19: 自联结sum指定不同条件查询数据; expect:成功
select aa.col_1,sum(aa.col_3)  from t_subpartition_0047 partition(p_list_2) aa,t_subpartition_0047 partition(p_list_2) bb  where aa.col_1=bb.col_3 and aa.col_2/10 >5 and aa.col_3 is not null group by aa.col_1;
--step20: 自联结指定条件查询数据; expect:成功
select * from t_subpartition_0047 partition(p_list_2) aa,t_subpartition_0047 partition(p_list_2) bb  where aa.col_1=bb.col_3 and aa.col_2 /10 >5 and aa.col_3 is not null ;
--step21: 插入数据; expect:成功
insert into t_subpartition_0047 values(15,9,1);
--step22: 自联结min指定条件数据; expect:成功，5条数据
select aa.col_1,min(bb.col_2)  from t_subpartition_0047 partition(p_list_2) aa,t_subpartition_0047 partition(p_list_2) bb  where aa.col_1=bb.col_3 and aa.col_3 is not null group by aa.col_1;

--step23: 删除表; expect:成功
drop table if exists t_subpartition_0047;
drop table if exists t_subpartition_0047_01;
drop tablespace if exists ts_subpartition_0047;