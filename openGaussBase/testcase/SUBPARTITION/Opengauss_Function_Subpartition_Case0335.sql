-- @testpoint: range_hash二级分区表：select 聚合函数/其他组合,部分测试点合理报错

--test1: select partition/subpartition for
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0335;
drop tablespace if exists ts_subpartition_0335;
create tablespace ts_subpartition_0335 relative location 'subpartition_tablespace/subpartition_tablespace_0335';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0335
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0335
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
     subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
    subpartition t_subpartition_0335
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0335 values(-15,1,1,1),(-4,1,4,4),(15,5,5,5),(18,8,8,8),(199,9,9,9);
insert into t_subpartition_0335 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0335 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step4: 查询一级分区数据; expect:成功
select * from t_subpartition_0335 partition for (5);
--step5: 查询二级分区数据; expect:成功
select * from t_subpartition_0335 subpartition for (199,9);

--test2: select 各种组合
--step6: 查询数据：subpartition/order by/desc; expect:成功
select * from t_subpartition_0335 subpartition(p_range_2_subpartdefault1) order by 1 desc,2;
--step7: 查询数据：subpartition/order by/desc/limit; expect:成功
select * from t_subpartition_0335 subpartition(p_range_2_subpartdefault1) order by 1 desc,2 limit 2,5;
--step8: 查询数据：subpartition/order by/desc/limit/offset; expect:成功
select * from t_subpartition_0335 subpartition(p_range_2_subpartdefault1) order by 1 desc limit 2 offset 3;
--step9: 查询数据：partition/order by/desc/limit/offset; expect:成功
select col_2 from t_subpartition_0335 partition(p_range_2) order by 1 desc limit 2 offset 3;
--step10: 自连接查询数据; expect:成功
select * from t_subpartition_0335  a,t_subpartition_0335 b  where a.col_1=b.col_2 and  a.col_1 >10;
--step11: 子查询查询数据; expect:成功
select * from (select * from t_subpartition_0335 subpartition(p_range_2_subpartdefault1))a,((select * from t_subpartition_0335 subpartition(p_range_5_subpartdefault1))) b  where a.col_1=b.col_2;

--test3: select 聚合函数：count/min/max/length/median...
--step12: 查询count一级分区数据; expect:成功
select count(*) from t_subpartition_0335 partition(p_range_1);
--step13: 查询count二级分区数据; expect:成功
select count(*) from t_subpartition_0335 subpartition(p_range_2_subpartdefault1);
--step14: 查询max/count/min/median二级分区数据; expect:成功
select max(col_2),count(*),min(col_1),median(col_4) from t_subpartition_0335 subpartition(p_range_2_subpartdefault1);
--step15: 查询length二级分区数据; expect:成功
select *,length(col_2),length(col_1) from t_subpartition_0335 subpartition(p_range_2_subpartdefault1);
--step16: 查询order by rownum desc limit一级分区数据; expect:成功
select rownum,* from t_subpartition_0335 partition(p_range_2) order by rownum desc limit 2,8;
--test4: select 其他组合
--step17: 查询二级分区数据:where/group by/order by/limit; expect:成功
select col_1 from t_subpartition_0335 subpartition(p_range_2_subpartdefault1) where col_2 >5  group by col_1 order by col_1 limit 10;
--step18: 查询二级分区数据:upper/order by/limit; expect:成功
select col_1,upper(col_3) from t_subpartition_0335 subpartition(p_range_2_subpartdefault1)   order by col_1 limit 10;
--step19: 查询表数据：count/as; expect:成功
select count(8) as "count" from  t_subpartition_0335;
--step20: 查询二级分区数据：order by/limit/for update; expect:成功
select col_1,upper(col_3) from t_subpartition_0335 subpartition(p_range_2_subpartdefault1)   order by col_1 limit 10 for update;
--step21: 查询二级分区数据：case/sum/group by; expect:成功
select case when col_1=1 then '男' else '女' end as "性别",sum(case when col_1<10 then 1 else 0 end) as "未成年",sum(case when col_1>=10 then 1 else 0 end) as "成年" from t_subpartition_0335 group by col_2,t_subpartition_0335.col_1;
--step22: 查询数据：where/子查询/max(定值); expect:成功
select * from t_subpartition_0335 where col_1=(select max(1) from t_subpartition_0335);
--step23: 查询数据：where/子查询/max(列); expect:成功
select * from t_subpartition_0335 where col_1 in (select max(col_1) from t_subpartition_0335);
--step24: 查询数据：子查询/order by/group by; expect:成功
select col_1,col_2 from (select * from t_subpartition_0335 order by col_2, col_3 desc) as tmp group by col_1,col_2;
--step25: 查询数据：表达式; expect:成功
select col_1< 60 from t_subpartition_0335;

--step26: 清理环境; expect:成功
drop table if exists t_subpartition_0335;
drop tablespace if exists ts_subpartition_0335;