-- @testpoint: 二级分区表序列最大值扩展

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0355;
drop tablespace if exists ts_subpartition_0355;
create tablespace ts_subpartition_0355 relative location 'subpartition_tablespace/subpartition_tablespace_0355';
--step2: 创建递增序列; expect:成功
drop sequence if exists seql_subpartition_0355;
create large sequence seql_subpartition_0355 start 170141183460469231731687303715884105720 ;
--step3: 创建range_range二级分区表; expect:成功
create table t_subpartition_0355
(
    col_1 numeric default nextval('seql_subpartition_0355'),
    col_2 numeric default nextval('seql_subpartition_0355'),
    col_3 numeric ,
    col_4 numeric
)
tablespace ts_subpartition_0355
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than(170141183460469231731687303715884105700)
  (
    subpartition p_range_1_1 values less than(170141183460469231731687303715884105710),
    subpartition p_range_1_2 values less than(170141183460469231731687303715884105726),
    subpartition p_range_1_3 values less than( maxvalue )
  ),
  partition p_range_2 values less than(170141183460469231731687303715884105710)
  (
    subpartition p_range_2_1 values less than(170141183460469231731687303715884105700),
    subpartition p_range_2_2 values less than(170141183460469231731687303715884105710),
    subpartition p_range_2_3 values less than(170141183460469231731687303715884105720),
    subpartition p_range_2_4 values less than(170141183460469231731687303715884105725),
    subpartition p_range_2_5 values less than( maxvalue )
  ),
   partition p_range_3 values less than(170141183460469231731687303715884105720)
   (subpartition p_range_3_5 values less than( maxvalue )
   ),
   partition p_range_4 values less than(170141183460469231731687303715884105725)
   (
    subpartition p_range_4_1 values less than(170141183460469231731687303715884105721),
    subpartition p_range_4_2 values less than(170141183460469231731687303715884105722),
    subpartition p_range_4_3 values less than(170141183460469231731687303715884105723),
    subpartition p_range_4_4 values less than(170141183460469231731687303715884105724),
    subpartition p_range_4_5 values less than( maxvalue )
   ),
   partition p_range_5 values less than(170141183460469231731687303715884105726),
   partition p_range_6 values less than( maxvalue )
);
--step4: 插入数据; expect:成功
insert into t_subpartition_0355(col_3) values(3),(3),(3),(3);
--step5: 查询数据; expect:成功,4条数据
select * from t_subpartition_0355;
--step6: 查询指定数据; expect:成功,1条数据
select * from t_subpartition_0355 subpartition(p_range_4_2);
--step7: 查询指定数据; expect:成功,0条数据
select * from t_subpartition_0355 subpartition(p_range_4_3);
--step8: 查询指定数据; expect:成功,1条数据
select * from t_subpartition_0355 subpartition(p_range_4_4);
--step9: 查询指定数据; expect:成功,1条数据
select * from t_subpartition_0355 subpartition(p_range_4_5);

--step10: 创建递减序列; expect:成功
drop table if exists t_subpartition_0355 cascade;
drop large sequence seql_subpartition_0355;
create large sequence seql_subpartition_0355 start -170141183460469231731687303715884105720  increment -1;
--step11: 创建range_range二级分区表,指定序列; expect:成功
create table t_subpartition_0355
(
    col_1 numeric default nextval('seql_subpartition_0355'),
    col_2 numeric default nextval('seql_subpartition_0355'),
    col_3 numeric ,
    col_4 numeric
)
tablespace ts_subpartition_0355
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than(-170141183460469231731687303715884105728)
  (
    subpartition p_range_1_1 values less than(-170141183460469231731687303715884105728),
    subpartition p_range_1_2 values less than(-170141183460469231731687303715884105726),
    subpartition p_range_1_3 values less than( maxvalue )
  ),
  partition p_range_2 values less than(-170141183460469231731687303715884105726)
  (
    subpartition p_range_2_1 values less than(-170141183460469231731687303715884105728),
    subpartition p_range_2_2 values less than(-170141183460469231731687303715884105726),
    subpartition p_range_2_3 values less than(-170141183460469231731687303715884105724),
    subpartition p_range_2_4 values less than(-170141183460469231731687303715884105723),
    subpartition p_range_2_5 values less than( maxvalue )
  ),
   partition p_range_3 values less than(-170141183460469231731687303715884105724)
   (subpartition p_range_3_5 values less than( maxvalue )
   ),
   partition p_range_4 values less than(-170141183460469231731687303715884105722)
   (
    subpartition p_range_4_1 values less than(-170141183460469231731687303715884105728),
    subpartition p_range_4_2 values less than(-170141183460469231731687303715884105726),
    subpartition p_range_4_3 values less than(-170141183460469231731687303715884105724),
    subpartition p_range_4_4 values less than(-170141183460469231731687303715884105723),
    subpartition p_range_4_5 values less than( maxvalue )
   ),
   partition p_range_5 values less than(-170141183460469231731687303715884105720),
   partition p_range_6 values less than( maxvalue )
);
--step12: 插入数据; expect:成功
insert into t_subpartition_0355(col_3) values(3),(3),(3),(3);
--step13: 查询数据; expect:成功
select * from t_subpartition_0355;
--step14: 将存储过程内语句返回的值存储到变量内; expect:成功
declare
v1 numeric[];
v2 numeric[];
begin
select col_1 bulk collect into v1  from t_subpartition_0355 partition(p_range_3);
select col_1 bulk collect into v2  from t_subpartition_0355 subpartition(p_range_4_3);
raise notice 'col_1 %',v1;
raise notice 'col_2 %',v2;
end;
/

--step15: 创建递减序列; expect:成功
drop table if exists t_subpartition_0355 cascade;
drop large sequence seql_subpartition_0355;
create large sequence seql_subpartition_0355 start -170141183460469231731687303715884105720  increment -1;
--step16: 创建hash_hash二级分区表; expect:成功
create table t_subpartition_0355
(
    col_1 numeric default nextval('seql_subpartition_0355') ,
    col_2 numeric default nextval('seql_subpartition_0355'),
    col_3 numeric,
    col_4 numeric
)
with(fillfactor=80)
partition by hash (col_1) subpartition by hash (col_2)
(
  partition p_range_1
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3,
    subpartition p_hash_1_4,
    subpartition p_hash_1_5,
    subpartition p_hash_1_6
  ),
  partition p_range_2,
  partition p_range_3
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
    subpartition p_hash_3_3
  ),
    partition p_range_4
  (
    subpartition p_hash_4_1
  ),
  partition p_range_5
) enable row movement;
--step17: 插入数据; expect:成功
insert into t_subpartition_0355(col_3) values(3),(3),(3),(3);
--step18: 查询指定数据; expect:成功
select * from t_subpartition_0355;
select * from t_subpartition_0355 subpartition(p_hash_4_1);
select * from t_subpartition_0355 subpartition(p_range_2_subpartdefault1);
select * from t_subpartition_0355 subpartition(p_hash_1_1);

--step19: 清理环境; expect:成功
drop table if exists t_subpartition_0355 cascade;
drop large sequence seql_subpartition_0355;
drop tablespace if exists ts_subpartition_0168;