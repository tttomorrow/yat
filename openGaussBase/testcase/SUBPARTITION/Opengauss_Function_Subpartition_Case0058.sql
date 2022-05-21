-- @testpoint: list_list二级分区表：触发器/函数/存储过程/游标

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0058;
drop tablespace if exists ts_subpartition_0058;
create tablespace ts_subpartition_0058 relative location 'subpartition_tablespace/subpartition_tablespace_0058';

--test1: 触发器
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0058
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0058
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
--step3: 创建函数，删除更新表数据; expect:成功
create or replace function func_tri_subpartition_0058() returns trigger
as $$
    declare
    begin
           delete from t_subpartition_0058;
           update t_subpartition_0058 set col_2 =10 where col_2=1;
           return new;
    end
$$ language plpgsql;
/
--step4: 创建触发器，与二级分区表关联，执行插入语句时后执行函数; expect:成功
create trigger tri_subpartition_0058
          after insert on t_subpartition_0058
          for each row
          execute procedure func_tri_subpartition_0058();
/
--step5: 插入数据; expect:成功
insert into t_subpartition_0058 values(1,1,1,1);
insert into t_subpartition_0058 values(1,1,1,1);
insert into t_subpartition_0058 values(2,2,2,2);
--step6: 查询表数据; expect:成功，无数据
select * from t_subpartition_0058;
drop function if exists func_tri_subpartition_0058() cascade;

--test2: 函数
--step7: 清空表数据; expect:成功
truncate t_subpartition_0058;
--step8: 创建函数，返回boolean值; expect:成功
drop function if exists func_subpartition_0058() cascade;
create or replace function func_subpartition_0058() returns boolean as
    $$
    declare
    begin
         delete from t_subpartition_0058 where col_2=8;
         return 1;
    end
    $$ language plpgsql;
    /
--step9: 创建函数，删除指定条件的数据，无返回值; expect:成功
drop function if exists func_subpartition_0058() cascade;
create or replace function func_subpartition_0058() returns void as
    $$
    declare
    begin
         delete from t_subpartition_0058 where col_2=8;
    end
    $$ language plpgsql;
    /
--step10: 创建函数，有返回值; expect:成功
drop function if exists func_subpartition_0058_01() cascade;
create or replace  function func_subpartition_0058_01()
returns table(col_1 int,col_2 int,col_3 varchar2 ( 30 ) ,col_4 int) as $$
begin
     return query select * from t_subpartition_0058;
end;
$$ language plpgsql;
/

--step11: 插入5条数据; expect:成功
insert into t_subpartition_0058 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step12: 调用函数; expect:成功，无数据
call func_subpartition_0058();
--step13: 调用函数; expect:成功，4条数据
call func_subpartition_0058_01();

--test3: 存储过程
--step14: 创建存储过程，删除指定数据; expect:成功
drop function if exists pro_subpartition_0058();
create or replace procedure pro_subpartition_0058 is
    begin
         delete from t_subpartition_0058 where col_2=8;
    end;
    /
--step15: 清空表数据数据; expect:成功
truncate t_subpartition_0058;
--step16: 插入5条数据; expect:成功
insert into t_subpartition_0058 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step17: 调用存储过程; expect:成功
call  pro_subpartition_0058();
--step18: 查询数据; expect:成功，4条数据
select * from t_subpartition_0058;

--test4: 游标
--step19: 清空表数据数据; expect:成功
truncate t_subpartition_0058;
--step20: 插入数据; expect:成功
insert into t_subpartition_0058 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step21: 插入数据; expect:成功
insert into t_subpartition_0058 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step22: 开启事务创建游标; expect:成功
begin;
cursor c1 for select * from t_subpartition_0058 subpartition (p_list_2_2);
fetch c1;
fetch c1;
fetch c1;
end;
/

--step23: 清理环境; expect:成功
drop function if exists func_subpartition_0058();
drop function if exists func_subpartition_0058_01();
drop function if exists func_tri_subpartition_0058() cascade;
drop function if exists pro_subpartition_0058();
drop table if exists t_subpartition_0058;
drop tablespace if exists ts_subpartition_0058;