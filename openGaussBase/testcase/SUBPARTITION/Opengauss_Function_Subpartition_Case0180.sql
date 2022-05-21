-- @testpoint: list_hash二级分区表：segment表/并行查询smp/package,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0180;
drop tablespace if exists ts_subpartition_0180;
create tablespace ts_subpartition_0180 relative location 'subpartition_tablespace/subpartition_tablespace_0180';
--test1: segment表
--step2: 创建二级分区表,指定segment=on; expect:成功
create table t_subpartition_0180
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)with (segment=on)
tablespace ts_subpartition_0180
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3
  )
) enable row movement ;
--step3: 插入大量数据; expect:成功
insert into t_subpartition_0180 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step4: 查询10行数据; expect:成功
select * from t_subpartition_0180 limit 10;

--test2: 并行查询smp
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0180;
create table t_subpartition_0180
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0180
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1 
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1 
  )
) enable row movement ;
--step6: 插入大量数据; expect:成功
insert into  t_subpartition_0180 values (generate_series(0, 19),generate_series(0, 2000),generate_series(0, 99));
--step7: 查看参数query_dop的值; expect:成功
show query_dop ;
--step8: 修改参数query_dop的值为2; expect:成功
set query_dop=2;
--step9: 查看执行计划; expect:成功
explain select * from t_subpartition_0180  a,t_subpartition_0180 b  where a.col_1=b.col_2 and  a.col_1 >10;

--test3: package
--step10: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0180;
create table t_subpartition_0180
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0180
partition by list (col_1) subpartition by hash (col_2)
(
  partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
    subpartition p_hash_1_3
  ),
  partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
  (
    subpartition p_hash_2_1 ,
    subpartition p_hash_2_2 ,
    subpartition p_hash_2_3 ,
    subpartition p_hash_2_4 ,
    subpartition p_hash_2_5
  ),
  partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
  partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
  (
    subpartition p_hash_4_1
  ),
  partition p_list_5 values (default)
  (
    subpartition p_hash_5_1
  ),
  partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_hash_6_1 ,
    subpartition p_hash_6_2 ,
    subpartition p_hash_6_3
  )
) enable row movement ;
--step11: 创建package1; expect:成功
drop package if exists pkg_subpartition_0180_01;
drop package if exists pkg_subpartition_0180_02;
create or replace package pkg_subpartition_0180_01 as
  function func_subpartition_0180_01(var1 int, var2 int) return int;
end pkg_subpartition_0180_01;
/
create or replace package body pkg_subpartition_0180_01 as
  function func_subpartition_0180_01(var1 int, var2 int) return int as
  begin
    raise info 'pkg_subpartition_0180_01.func_subpartition_0180_01 is called';
    insert into t_subpartition_0180 values(var1,var2);
    update t_subpartition_0180 set col_2=8 where col_2=4;
    return 0;
  end;
end pkg_subpartition_0180_01;
/
--step12: 创建package2; expect:成功
create or replace package pkg_subpartition_0180_02 as
  function func_subpartition_0180_02(var1 int, var2 int) return int;
end pkg_subpartition_0180_02;
/
create or replace package body pkg_subpartition_0180_02 as
  function func_subpartition_0180_02(var1 int, var2 int) return int as
  begin
    raise info 'pkg_subpartition_0180_02.func_subpartition_0180_02 is called';
    insert into t_subpartition_0180 values(var1,var2);
    delete t_subpartition_0180 where col_2=8;
    return 0;
  end;
end pkg_subpartition_0180_02;
/
--step13: 调用package1; expect:成功
call pkg_subpartition_0180_01.func_subpartition_0180_01(4,4);
--step14: 调用package2; expect:成功
call pkg_subpartition_0180_02.func_subpartition_0180_02(5,5);
--step15: 查询数据; expect:成功,1条数据
select * from t_subpartition_0180 ;
--step16: 查询系统表数据; expect:成功,2条数据
select pkgname,pkgspecsrc,pkgbodydeclsrc from gs_package;

--step17: 删除package; expect:成功
drop package if exists pkg_subpartition_0180_01;
drop package if exists pkg_subpartition_0180_02;
--step18: 清理环境; expect:成功
drop table if exists t_subpartition_0180;
drop tablespace if exists ts_subpartition_0180;