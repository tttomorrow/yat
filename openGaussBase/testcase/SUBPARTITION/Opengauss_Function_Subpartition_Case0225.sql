-- @testpoint: range_list二级分区表：select 聚合函数/其他组合

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0225_01;
drop table if exists t_subpartition_0225;
drop tablespace if exists ts_subpartition_0225;
create tablespace ts_subpartition_0225 relative location 'subpartition_tablespace/subpartition_tablespace_0225';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0225
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0225
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
insert into t_subpartition_0225 values(-15,1,1,1),(-4,1,4,4),(15,5,5,5),(18,8,8,8),(199,9,9,9);
insert into t_subpartition_0225 values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0225 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0225 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);

--test1: select 聚合函数：count/min/max/length/median...
--step4: 查询count一级分区数据; expect:成功
select count(*) from t_subpartition_0225 partition(p_range_1);
--step5: 查询count二级分区数据; expect:成功
select count(*) from t_subpartition_0225 subpartition(p_list_2_2);
--step6: 查询max/count/min/median二级分区数据; expect:成功
select max(col_2),count(*),min(col_1),median(col_4) from t_subpartition_0225 subpartition(p_list_2_2);
--step7: 查询length二级分区数据; expect:成功
select *,length(col_2),length(col_1) from t_subpartition_0225 subpartition(p_list_2_2);
--step8: 查询order by rownum desc limit一级分区数据; expect:成功
select rownum,* from t_subpartition_0225 partition(p_range_2) order by rownum desc limit 2,8;
--test2: select 其他组合
--step9: 查询二级分区数据:where/group by/order by/limit; expect:成功
select col_1 from t_subpartition_0225 subpartition(p_list_2_2) where col_2 >5  group by col_1 order by col_1 limit 10;
--step10: 查询二级分区数据:upper/order by/limit; expect:成功
select col_1,upper(col_3) from t_subpartition_0225 subpartition(p_list_2_2)   order by col_1 limit 10;
--step11: 查询表数据：count/as; expect:成功
select count(8) as "count" from  t_subpartition_0225;
--step12: 查询二级分区数据：order by/limit/for update; expect:成功
select col_1,upper(col_3) from t_subpartition_0225 subpartition(p_list_2_2)   order by col_1 limit 10 for update;
--step13: 查询二级分区数据：case/sum/group by; expect:成功
select case when col_1=1 then '男' else '女' end as "性别",sum(case when col_1<10 then 1 else 0 end) as "未成年",sum(case when col_1>=10 then 1 else 0 end) as "成年" from t_subpartition_0225 group by col_2,t_subpartition_0225.col_1;
--step14: 查询数据：where/子查询/max(定值); expect:成功
select * from t_subpartition_0225 where col_1=(select max(1) from t_subpartition_0225);
--step15: 查询数据：where/子查询/max(列); expect:成功
select * from t_subpartition_0225 where col_1 in (select max(col_1) from t_subpartition_0225);
--step16: 查询数据：子查询/order by/group by; expect:成功
select col_1,col_2 from (select * from t_subpartition_0225 order by col_2, col_3 desc) as tmp group by col_1,col_2;
--step17: 查询数据：表达式; expect:成功
select col_1< 60 from t_subpartition_0225;
--step18: substr查询数据; expect:成功
select substr(col_2,1,2) from t_subpartition_0225;
--step19: abs查询数据; expect:成功
select abs(col_1) from t_subpartition_0225;
--step20: select into查询数据; expect:成功
drop table if exists t_subpartition_0225_01;
select col_1 into t_subpartition_0225_01 from t_subpartition_0225  where col_1 in (select abs(col_1) from t_subpartition_0225) ;
select * from t_subpartition_0225_01 where col_1>0;
--step21: abs/表达式查询数据; expect:成功
select col_1 >0 from t_subpartition_0225  where col_1 in (select abs(col_1) from t_subpartition_0225) ;
--step22: 不同的表达式查询数据; expect:成功
select distinct(to_integer(col_1::varchar(20))) >=0 from t_subpartition_0225  where col_1 in (select abs(col_1) from t_subpartition_0225) group by col_1;

--step23: 清理环境; expect:成功
drop table if exists t_subpartition_0225_01;
drop table if exists t_subpartition_0225;
drop tablespace if exists ts_subpartition_0225;