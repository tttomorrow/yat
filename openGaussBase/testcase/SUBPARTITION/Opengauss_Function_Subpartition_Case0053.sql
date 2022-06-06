-- @testpoint: list_list二级分区表：select 聚合函数/其他组合

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0053;
drop tablespace if exists ts_subpartition_0053;
create tablespace ts_subpartition_0053 relative location 'subpartition_tablespace/subpartition_tablespace_0053';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0053
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0053
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0053 values(-15,1,1,1),(-4,1,4,4),(15,5,5,5),(18,8,8,8),(199,9,9,9);
insert into t_subpartition_0053 values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0053 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0053 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);

--test1: select 聚合函数：count/min/max/length/median...
--step4: 查询count一级分区数据; expect:成功
select count(*) from t_subpartition_0053 partition(p_list_1);
--step5: 查询count二级分区数据; expect:成功
select count(*) from t_subpartition_0053 subpartition(p_list_2_1);
--step6: 查询max/count/min/median二级分区数据; expect:成功
select max(col_2),count(*),min(col_1),median(col_4) from t_subpartition_0053 subpartition(p_list_2_1);
--step7: 查询length二级分区数据; expect:成功
select *,length(col_2),length(col_1) from t_subpartition_0053 subpartition(p_list_2_1);
--step8: 查询order by rownum desc limit一级分区数据; expect:成功
select rownum,* from t_subpartition_0053 partition(p_list_2) order by rownum desc limit 2,8;

--test2: select 其他组合
--step9: 查询二级分区数据:where/group by/order by/limit; expect:成功
select col_1 from t_subpartition_0053 subpartition(p_list_2_2) where col_2 >5  group by col_1 order by col_1 limit 10;
--step10: 查询二级分区数据:upper/order by/limit; expect:成功
select col_1,upper(col_3) from t_subpartition_0053 subpartition(p_list_2_2)   order by col_1 limit 10;
--step11: 查询表数据：count/as; expect:成功
select count(8) as "count" from  t_subpartition_0053;
--step12: 查询二级分区数据：order by/limit/for update; expect:成功
select col_1,upper(col_3) from t_subpartition_0053 subpartition(p_list_2_2)   order by col_1 limit 10 for update;
--step13: 查询二级分区数据：case/sum/group by; expect:成功
select case when col_1=1 then '男' else '女' end as "性别",sum(case when col_1<10 then 1 else 0 end) as "未成年",sum(case when col_1>=10 then 1 else 0 end)
as "成年" from t_subpartition_0053 group by col_2,t_subpartition_0053.col_1;
--step14: 查询数据：where/子查询/max(定值); expect:成功
select * from t_subpartition_0053 where col_1=(select max(1) from t_subpartition_0053);
--step15: 查询数据：where/子查询/max(列); expect:成功
select * from t_subpartition_0053 where col_1 in (select max(col_1) from t_subpartition_0053);
--step16: 查询数据：子查询/order by/group by; expect:成功
select col_1,col_2 from (select * from t_subpartition_0053 order by col_2, col_3 desc) as tmp group by col_1,col_2;
--step17: 查询数据：表达式; expect:成功
select col_1< 60 from t_subpartition_0053;

--step18: 删除表; expect:成功
drop table if exists t_subpartition_0053;
drop tablespace if exists ts_subpartition_0053;