-- @testpoint: list_range二级分区表：自治事务/匿名块

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0126;
drop tablespace if exists ts_subpartition_0126;
create tablespace ts_subpartition_0126 relative location 'subpartition_tablespace/subpartition_tablespace_0126';
--test1: 自治事务
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0126
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0126
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0126 values(1,2);
--step4: 查询数据; expect:成功
select * from t_subpartition_0126;
--step5: 创建包含自治事务的存储过程; expect:成功
drop function if exists autonomous_4();
create or replace procedure autonomous_4(a int, b int) as
declare
num3 int := a;
num4 int := b;
pragma autonomous_transaction;
begin
insert into t_subpartition_0126 values(num3, num4);
end;
/
--step6: 创建调用自治事务存储过程的普通存储过程; expect:成功
drop function if exists autonomous_5();
create or replace procedure autonomous_5(a int, b int) as
declare
begin
insert into t_subpartition_0126 values(66, 66);
autonomous_4(a,b);
rollback;
end;
/
--step7: 调用普通存储过程; expect:成功
select autonomous_5(11,22);
--step8: 查看表结果; expect:成功，2条数据
select * from t_subpartition_0126 order by col_1;
--step9: 删除函数; expect:成功
drop function if exists autonomous_4();
drop function if exists autonomous_5();

--test2: 匿名块
--step10: 创建匿名块; expect:成功
start transaction;
declare
pragma autonomous_transaction;
begin
insert into t_subpartition_0126 values(1,2,'you are so cute,will commit!');
end;
/
--step11: 插入数据; expect:成功
insert into t_subpartition_0126 values(1,4,'you will rollback!');
--step12: 回滚当前事务并取消当前事务中的所有更新; expect:成功
rollback;
--step13: 查询数据; expect:成功，3条数据
select * from t_subpartition_0126;


--test3: 函数
--step14: 创建函数; expect:成功
drop function if exists autonomous_32();
create or replace function autonomous_32(a int ,b int ,c text) return int as
declare
pragma autonomous_transaction;
begin
insert into t_subpartition_0126 values(a, b, c);
return 1;
end;
/
--step15: 创建函数; expect:成功
drop function if exists autonomous_33();
create or replace function autonomous_33(num1 int) return int as
declare
num3 int := 22;
tmp int;
pragma autonomous_transaction;
begin
num3 := num3/num1;
return num3;
exception
when division_by_zero then
select autonomous_32(num3, num1, sqlerrm) into tmp;
return 0;
end;
/
--step16: 调用函数; expect:成功
select autonomous_33(0);
--step17: 查询数据; expect:成功，4条数据
select * from t_subpartition_0126;
--step18: 删除函数; expect:成功，4条数据
drop function if exists autonomous_32();
drop function if exists autonomous_33();

--step19: 清理环境; expect:成功
drop table if exists t_subpartition_0126_01;
drop table if exists t_subpartition_0126;
drop tablespace if exists ts_subpartition_0126;