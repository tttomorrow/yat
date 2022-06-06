-- @testpoint: range_list二级分区表：select,部分测试点合理报错

--test1: select partition/subpartition for
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0223;
drop tablespace if exists ts_subpartition_0223;
create tablespace ts_subpartition_0223 relative location 'subpartition_tablespace/subpartition_tablespace_0223';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0223
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0223
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0223 values(-15,1,1,1),(-4,1,4,4),(15,5,5,5),(18,8,8,8),(199,9,9,9);
insert into t_subpartition_0223 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0223 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step4: 查询一级分区数据; expect:成功
select * from t_subpartition_0223 partition for (5);
--step5: 查询二级分区数据; expect:成功
select * from t_subpartition_0223 subpartition for (5,5);

--test2: select 各种组合
--step6: 查询数据：subpartition/order by/desc; expect:成功
select * from t_subpartition_0223 subpartition(p_list_2_2) order by 1 desc,2;
--step7: 查询数据：subpartition/order by/desc/limit; expect:成功
select * from t_subpartition_0223 subpartition(p_list_2_2) order by 1 desc,2 limit 2,5;
--step8: 查询数据：subpartition/order by/desc/limit/offset; expect:成功
select * from t_subpartition_0223 subpartition(p_list_2_2) order by 1 desc,2 limit 2 offset 3;
--step9: 查询数据：partition/order by/desc/limit/offset; expect:成功
select col_2 from t_subpartition_0223 partition(p_range_2) order by 1 desc limit 2 offset 3;
--step10: 自连接查询数据; expect:成功
select * from t_subpartition_0223  a,t_subpartition_0223 b  where a.col_1=b.col_2 and  a.col_1 >10;
--step11: 子查询查询数据; expect:成功
select * from (select * from t_subpartition_0223 subpartition(p_list_2_2))a,((select * from t_subpartition_0223 subpartition(p_list_2_1))) b  where a.col_1=b.col_2;

--step12: 清理环境; expect:成功
drop table if exists t_subpartition_0223;
drop tablespace if exists ts_subpartition_0223;