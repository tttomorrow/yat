-- @testpoint: list_list二级分区表：segment表/并行查询smp/package,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0066;
drop tablespace if exists ts_subpartition_0066;
create tablespace ts_subpartition_0066 relative location 'subpartition_tablespace/subpartition_tablespace_0066';
--test1: segment表
--step2: 创建二级分区表，指定segment=on; expect:成功
create table t_subpartition_0066
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)with (segment=on)
tablespace ts_subpartition_0066
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
--step3: 插入大量数据; expect:成功
insert into t_subpartition_0066 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step4: 查询10行数据; expect:成功
select * from t_subpartition_0066 limit 10;

--test2: 并行查询smp
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0066;
create table t_subpartition_0066
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0066
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(default),
  partition p_list_2 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_2_1 values ( default )
  )
) enable row movement;
--step6: 插入大量数据; expect:成功
insert into  t_subpartition_0066 values (generate_series(0, 19),generate_series(0, 2000),generate_series(0, 99));
--step7: 查看参数query_dop的值; expect:成功
show query_dop ;
--step8: 修改参数query_dop的值为2; expect:成功
set query_dop=2;
--step9: 查看执行计划; expect:成功
explain select * from t_subpartition_0066  a,t_subpartition_0066 b  where a.col_1=b.col_2 and  a.col_1 >10;

--test3: package
--step10: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0066;
create table t_subpartition_0066
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0066
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
--step11: 创建package1; expect:成功
drop package if exists pkg1;
drop package if exists pkg2;
create or replace package pkg1 as
  function func(var1 int, var2 int) return int;
end pkg1;
/
create or replace package body pkg1 as
  function func(var1 int, var2 int) return int as
  begin
    raise info 'pkg1.func is called';
    insert into t_subpartition_0066 values(var1,var2);
    update t_subpartition_0066 set col_2=8 where col_2=4;
    return 0;
  end;
end pkg1;
/
--step12: 创建package2; expect:成功
create or replace package pkg2 as
  function func1(var1 int, var2 int) return int;
end pkg2;
/
create or replace package body pkg2 as
  function func1(var1 int, var2 int) return int as
  begin
    raise info 'pkg2.func1 is called';
    insert into t_subpartition_0066 values(var1,var2);
    delete t_subpartition_0066 where col_2=8;
    return 0;
  end;
end pkg2;
/
--step13: 调用package1; expect:成功
call pkg1.func(4,4);
--step14: 调用package2; expect:成功
call pkg2.func1(5,5);
--step15: 查询数据; expect:成功，1条数据
select * from t_subpartition_0066 ;
--step16: 查询系统表数据; expect:成功，2条数据
select pkgname,pkgspecsrc,pkgbodydeclsrc from gs_package;

--step17: 删除package; expect:成功
drop package if exists pkg1;
drop package if exists pkg2;
--step18: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0066;
drop tablespace if exists ts_subpartition_0066;