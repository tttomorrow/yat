-- @testpoint: range_hash二级分区表：分区列序列

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0338;
drop tablespace if exists ts_subpartition_0338;
create tablespace ts_subpartition_0338 relative location 'subpartition_tablespace/subpartition_tablespace_0338';

--test1: 序列--分区列序列,声明分区键的类型为序列整型
--step2: 创建二级分区表,声明分区键的类型为序列整型; expect:成功
create table if not exists t_subpartition_0338
(
    col_1 serial ,
    col_2 serial,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0338
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
    subpartition t_subpartition_0338
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0338(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step4: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0338 subpartition(p_range_2_subpartdefault1);
--step5: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0338 truncate subpartition p_range_2_subpartdefault1;
--step6: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0338 subpartition(p_range_2_subpartdefault1);
--step7: 插入数据; expect:成功
insert into t_subpartition_0338(col_2,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0338(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step8: 查询数据; expect:成功,有数据
select * from t_subpartition_0338 subpartition(p_range_2_subpartdefault1);

--test2: 序列--分区列序列,指定序列与列的归属关系
--step9: 创建序列; expect:成功
drop sequence if exists seql_subpartition_0338;
create sequence seql_subpartition_0338 cache 100;
--step10: 创建二级分区表,将序列值作为分区键的默认值,使该字段具有唯一标识属性; expect:成功
drop table if exists t_subpartition_0338;
create table if not exists t_subpartition_0338
(
    col_1 int not null default nextval('seql_subpartition_0338'),
    col_2 int  not null default nextval('seql_subpartition_0338'),
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0338
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
    subpartition t_subpartition_0338
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step11: 指定序列与列的归属关系; expect:成功
alter sequence seql_subpartition_0338 owned by t_subpartition_0338.col_2;
alter sequence seql_subpartition_0338 owned by t_subpartition_0338.col_1;
--step12: 插入数据; expect:成功
insert into t_subpartition_0338(col_1,col_3,col_4) values(-11,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0338(col_2,col_3,col_4) values(-11,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0338(col_1,col_3,col_4) values(-11,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0338(col_2,col_3,col_4) values(-11,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);

--step13: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0338 subpartition(p_range_2_subpartdefault1);
--step14: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0338 truncate subpartition p_range_2_subpartdefault1;
--step15: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0338 subpartition(p_range_2_subpartdefault1);
--step16: 插入数据; expect:成功
insert into t_subpartition_0338(col_1,col_3,col_4) values(-11,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0338(col_2,col_3,col_4) values(-11,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step17: 查询数据; expect:成功
select * from t_subpartition_0338 ;
--step18: 查询数据; expect:成功,有数据
select * from t_subpartition_0338 subpartition(p_range_2_subpartdefault1);
 --step19: 查询数据; expect:成功
select * from t_subpartition_0338 subpartition(p_hash_3_1);

--step20: 清理环境; expect:成功
drop table if exists t_subpartition_0338;
drop tablespace if exists ts_subpartition_0338;