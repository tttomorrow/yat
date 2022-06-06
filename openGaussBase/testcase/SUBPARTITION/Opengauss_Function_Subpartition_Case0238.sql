-- @testpoint: range_list二级分区表：segment表/并行查询smp/package,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0238;
drop tablespace if exists ts_subpartition_0238;
create tablespace ts_subpartition_0238 relative location 'subpartition_tablespace/subpartition_tablespace_0238';
--test1: segment表
--step2: 创建二级分区表,指定segment=on; expect:成功
create table t_subpartition_0238
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)with (segment=on)
tablespace ts_subpartition_0238
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values less than( 50 ),
    subpartition p_list_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values less than( 50 ),
    subpartition p_list_2_2 values less than( maxvalue )
  )
);
--step3: 创建二级分区表,指定hashbucket=on; expect:合理报错
drop table if exists t_subpartition_0238;
create table t_subpartition_0238
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int ,
    primary key(col_1,col_2)
)with (hashbucket=on)
tablespace ts_subpartition_0238
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

--test2: 并行查询smp
--step4: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0238;
create table t_subpartition_0238
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0238
partition by range (col_1) subpartition by list (col_2)
(
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step5: 插入大量数据; expect:成功
insert into  t_subpartition_0238 values (generate_series(0, 39),generate_series(0, 2000),generate_series(0, 99));
--step6: 查看参数query_dop的值; expect:成功
show query_dop ;
--step7: 修改参数query_dop的值为2; expect:成功
set query_dop=2;
--step8: 查看执行计划; expect:成功
explain select * from t_subpartition_0238  a,t_subpartition_0238 b  where a.col_1=b.col_2 and  a.col_1 >10;

--test3: package
--step9: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0238;
create table t_subpartition_0238
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0238
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
--step10: 创建package1; expect:成功
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
    insert into t_subpartition_0238 values(var1,var2);
    update t_subpartition_0238 set col_2=8 where col_2=4;
    return 0;
  end;
end pkg1;
/
--step11: 创建package2; expect:成功
create or replace package pkg2 as
  function func1(var1 int, var2 int) return int;
end pkg2;
/
create or replace package body pkg2 as
  function func1(var1 int, var2 int) return int as
  begin
    raise info 'pkg2.func1 is called';
    insert into t_subpartition_0238 values(var1,var2);
    delete t_subpartition_0238 where col_2=8;
    return 0;
  end;
end pkg2;
/
--step12: 调用package1; expect:成功
call pkg1.func(4,4);
--step13: 调用package2; expect:成功
call pkg2.func1(5,5);
--step14: 查询数据; expect:成功
select * from t_subpartition_0238 ;
--step16: 查询系统表数据; expect:成功,2条数据
select pkgname,pkgspecsrc,pkgbodydeclsrc from gs_package;

--step16: 删除package; expect:成功
drop package if exists pkg1;
drop package if exists pkg2;
--step17: 清理环境; expect:成功
drop table if exists t_subpartition_0238;
drop tablespace if exists ts_subpartition_0238;