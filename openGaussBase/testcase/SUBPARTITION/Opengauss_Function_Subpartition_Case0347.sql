-- @testpoint: range_hash二级分区表：自治事务/匿名块

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0347;
drop tablespace if exists ts_subpartition_0347;
create tablespace ts_subpartition_0347 relative location 'subpartition_tablespace/subpartition_tablespace_0347';
--test1: 自治事务
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0347
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0347
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
    subpartition t_subpartition_0347
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0347 values(1,2);
--step4: 查询数据; expect:成功
select * from t_subpartition_0347;
--step5: 创建包含自治事务的存储过程; expect:成功
drop function if exists autonomous_4();
create or replace procedure autonomous_4(a int, b int) as
declare
num3 int := a;
num4 int := b;
pragma autonomous_transaction;
begin
insert into t_subpartition_0347 values(num3, num4);
end;
/
--step6: 创建调用自治事务存储过程的普通存储过程; expect:成功
drop function if exists autonomous_5();
create or replace procedure autonomous_5(a int, b int) as
declare
begin
insert into t_subpartition_0347 values(66, 66);
autonomous_4(a,b);
rollback;
end;
/
--step7: 调用普通存储过程; expect:成功
select autonomous_5(11,22);
--step8: 查看表结果; expect:成功,2条数据
select * from t_subpartition_0347 order by col_1;
--step9: 删除函数; expect:成功
drop function if exists autonomous_4();
drop function if exists autonomous_5();

--test2: 匿名块
--step10: 创建匿名块; expect:成功
start transaction;
declare
pragma autonomous_transaction;
begin
insert into t_subpartition_0347 values(1,2,'you are so cute,will commit!');
end;
/
--step11: 插入数据; expect:成功
insert into t_subpartition_0347 values(1,4,'you will rollback!');
--step12: 回滚当前事务并取消当前事务中的所有更新; expect:成功
rollback;
--step13: 查询数据; expect:成功,3条数据
select * from t_subpartition_0347;


--test3: 函数
--step14: 创建函数; expect:成功
drop function if exists autonomous_32();
create or replace function autonomous_32(a int ,b int ,c text) return int as
declare
pragma autonomous_transaction;
begin
insert into t_subpartition_0347 values(a, b, c);
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
--step17: 查询数据; expect:成功,4条数据
select * from t_subpartition_0347;
--step18: 删除函数; expect:成功,4条数据
drop function if exists autonomous_32();
drop function if exists autonomous_33();

--step19: 清理环境; expect:成功
drop table if exists t_subpartition_0347_01;
drop table if exists t_subpartition_0347;
drop tablespace if exists ts_subpartition_0347;