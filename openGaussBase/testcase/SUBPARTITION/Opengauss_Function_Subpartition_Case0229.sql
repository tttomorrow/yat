-- @testpoint: range_list二级分区表：分区列序列

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0229;
drop tablespace if exists ts_subpartition_0229;
create tablespace ts_subpartition_0229 relative location 'subpartition_tablespace/subpartition_tablespace_0229';

--test1: 序列--分区列序列,声明分区键的类型为序列整型
--step2: 创建二级分区表,声明分区键的类型为序列整型; expect:成功
create table if not exists t_subpartition_0229
(
    col_1 int ,
    col_2 serial, 
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0229
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
insert into t_subpartition_0229(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step4: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0229 subpartition(p_list_2_2);
--step5: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0229 truncate subpartition p_list_2_2;
--step6: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0229 subpartition(p_list_2_2);
--step7: 插入数据; expect:成功
insert into t_subpartition_0229(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step8: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0229 subpartition(p_list_2_2);
--step9: 查询数据; expect:成功
select * from t_subpartition_0229;
--step10: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0229 subpartition(p_list_3_1);
--step11: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0229 subpartition(p_list_2_1);

--test2: 序列--分区列序列,指定序列与列的归属关系
--step12: 创建序列; expect:成功
drop sequence if exists seql_subpartition_0229;
create sequence seql_subpartition_0229 cache 100;
--step13: 创建二级分区表,将序列值作为分区键的默认值,使该字段具有唯一标识属性; expect:成功
create table if not exists t_subpartition_0229
(
    col_1 int ,
    col_2 int  not null default nextval('seql_subpartition_0229'),
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0229
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
--step14: 指定序列与列的归属关系; expect:成功
alter sequence seql_subpartition_0229 owned by t_subpartition_0229.col_2;
--step15: 插入数据; expect:成功
insert into t_subpartition_0229(col_1,col_3,col_4) values(-11,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);

--step16: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0229 subpartition(p_list_2_1);
--step17: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0229 subpartition(p_list_2_2);
--step18: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0229 truncate subpartition p_list_2_1;
--step19: 查询指定二级分区数据; expect:成功,无数据
select * from t_subpartition_0229 subpartition(p_list_2_1);
--step20: 查询指定二级分区数据; expect:成功,有数据
select * from t_subpartition_0229 subpartition(p_list_2_2);
--step21: 插入数据; expect:成功
insert into t_subpartition_0229(col_1,col_3,col_4) values(1,1,1),(4,1,4),(5,5,5),(8,8,8),(9,9,9);
--step22: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0229 subpartition(p_list_2_1);
--step23: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0229 subpartition(p_list_2_2);

--step24: 创建序列; expect:成功
drop sequence if exists seql_subpartition_0229_01;
create sequence seql_subpartition_0229_01 minvalue 1 maxvalue 9999999999 increment by 1 start with 1 cache 500;
--step25: 插入序列数据; expect:成功
insert into t_subpartition_0229 values(seql_subpartition_0229_01.nextval,seql_subpartition_0229_01.nextval,seql_subpartition_0229_01.nextval);

--step26: 清理环境; expect:成功
drop table if exists t_subpartition_0229;
drop tablespace if exists ts_subpartition_0229;