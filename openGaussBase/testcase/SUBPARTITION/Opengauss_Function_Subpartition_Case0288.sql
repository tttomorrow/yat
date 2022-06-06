-- @testpoint: range_range二级分区表：非分区列序列

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0288;
drop tablespace if exists ts_subpartition_0288;
create tablespace ts_subpartition_0288 relative location 'subpartition_tablespace/subpartition_tablespace_0288';

--test1: 序列--非分区列序列,声明非分区键的类型为序列整型
--step2: 创建二级分区表,声明非分区键的类型为序列整型; expect:成功
create table if not exists t_subpartition_0288
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 serial
)tablespace ts_subpartition_0288
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0288 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step4: 查询表数据; expect:成功,有数据
select * from t_subpartition_0288;
--step5: 清空表数据; expect:成功
truncate t_subpartition_0288;
--step6: 查询表数据; expect:成功,无数据
select * from t_subpartition_0288;

--step7: 插入数据; expect:成功
insert into t_subpartition_0288 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step8: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288;
--step9: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0288 truncate subpartition p_range_1_1;
--step10: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0288 subpartition(p_range_1_1);
--step11: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288 subpartition(p_range_1_2);

--step12: 插入数据; expect:成功
insert into t_subpartition_0288 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step13: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288 subpartition(p_range_1_1);
--step14: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288 subpartition(p_range_1_2);

--test2: 序列--非分区列序列,指定序列与列的归属关系
--step15: 创建序列; expect:成功
drop sequence if exists seql_subpartition_0288;
create sequence seql_subpartition_0288 cache 100;
--step16: 创建二级分区表,将序列值作为非分区列的默认值,使该字段具有唯一标识属性; expect:成功
drop table if exists t_subpartition_0288;
create table if not exists t_subpartition_0288
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int not null default nextval('seql_subpartition_0288')
)tablespace ts_subpartition_0288
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step17: 指定序列与列的归属关系; expect:成功
alter sequence seql_subpartition_0288 owned by t_subpartition_0288.col_4;
--step18: 插入数据; expect:成功
insert into t_subpartition_0288 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);

--step19: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288 subpartition(p_range_1_1);
--step20: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288 subpartition(p_range_1_2);
--step21: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0288 truncate subpartition p_range_1_1;
--step22: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0288 subpartition(p_range_1_1);
--step23: 插入数据; expect:成功
insert into t_subpartition_0288 values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step24: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288 subpartition(p_range_1_1);
--step25: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0288 subpartition(p_range_1_2);

--step26: 清理环境; expect:成功
drop table if exists t_subpartition_0288;
drop tablespace if exists ts_subpartition_0288;