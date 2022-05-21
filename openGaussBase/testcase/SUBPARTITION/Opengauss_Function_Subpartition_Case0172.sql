-- @testpoint: list_hash二级分区表：触发器/函数/存储过程/游标

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0172;
drop tablespace if exists ts_subpartition_0172;
create tablespace ts_subpartition_0172 relative location 'subpartition_tablespace/subpartition_tablespace_0172';

--test1: 触发器
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0172
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0172
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
--step3: 创建函数,删除更新表数据; expect:成功
drop function if exists func_tri_subpartition_0172() cascade;
create or replace function func_tri_subpartition_0172() returns trigger as
           $$
           declare
           begin
                   delete from t_subpartition_0172; 
                   update t_subpartition_0172 set col_2 =10 where col_2=1;
                   return new;
           end
           $$ language plpgsql;
           /
--step4: 创建触发器,与二级分区表关联,执行插入语句时后执行函数; expect:成功
create trigger tri_subpartition_0172
          after insert on t_subpartition_0172
          for each row
          execute procedure func_tri_subpartition_0172();
          /
--step5: 插入数据; expect:成功
insert into t_subpartition_0172 values(1,1,1,1);
--step6: 查询表数据; expect:成功,无数据
select * from t_subpartition_0172;
--step7: 插入数据; expect:成功
insert into t_subpartition_0172 values(2,2,2,2);
--step8: 查询表数据; expect:成功,无数据
select * from t_subpartition_0172;
--step9: 删除函数; expect:成功
drop function if exists func_tri_subpartition_0172() cascade;

--test2: 函数
--step10: 清空表数据; expect:成功
truncate t_subpartition_0172;
--step11: 创建函数,返回boolean值; expect:成功
drop function if exists func_subpartition_0172() cascade;
create or replace function func_subpartition_0172() returns boolean as
    $$
    declare
    begin
         delete from t_subpartition_0172 where col_2=8;
         return 1;
    end
    $$ language plpgsql;
    /
--step12: 创建函数,删除指定条件的数据,无返回值; expect:成功
drop function if exists func_subpartition_0172() cascade;
create or replace function func_subpartition_0172() returns void as
    $$
    declare
    begin
         delete from t_subpartition_0172 where col_2=8;
    end
    $$ language plpgsql;
    /
--step13: 创建函数,有返回值; expect:成功
drop function if exists func_subpartition_0172_01() cascade;
create or replace  function func_subpartition_0172_01()
returns table(col_1 int,col_2 int,col_3 varchar2 ( 30 ) ,col_4 int) as $$
begin
     return query select * from t_subpartition_0172;
end;
$$ language plpgsql;
/

--step14: 插入数据; expect:成功
insert into t_subpartition_0172 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step15: 调用函数; expect:成功,无数据
call func_subpartition_0172();
--step16: 调用函数; expect:成功,4条数据
call func_subpartition_0172_01();

--test3: 存储过程
--step17: 创建存储过程,删除指定数据; expect:成功
drop function if exists pro_subpartition_0172();
create or replace procedure pro_subpartition_0172 is
    begin
         delete from t_subpartition_0172 where col_2=8;
    end;
    /
--step18: 清空表数据; expect:成功
truncate t_subpartition_0172;
--step19: 插入5条数据; expect:成功
insert into t_subpartition_0172 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step20: 调用存储过程; expect:成功
call  pro_subpartition_0172();
--step21: 查询数据; expect:成功,4条数据
select * from t_subpartition_0172;

--test4: 游标
--step22: 清空表数据; expect:成功
truncate t_subpartition_0172;
--step23: 插入数据; expect:成功
insert into t_subpartition_0172 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0172 values(81,1,1,1),(84,1,4,4),(85,5,5,5),(88,8,8,8),(89,1,9,9);
--step24: 开启事务创建游标; expect:成功
begin;
cursor c1 for select * from t_subpartition_0172 subpartition (p_hash_5_1);
fetch c1;
fetch c1;
fetch c1;
end;
/


--step25: 创建普通表; expect:成功
drop function if exists pro_subpartition_0172();
drop table if exists t_subpartition_0172;
create table if not exists t_subpartition_0172
(
    col_1 int ,
    col_2 nvarchar2 (9999999),
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0172;
--step26: 插入数据; expect:成功
insert into t_subpartition_0172 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0172 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step27: 开启事务创建游标; expect:成功
begin;
cursor c1 for select * from t_subpartition_0172 where col_1>18;
fetch c1;
fetch c1;
fetch c1;
end;
/

--step28: 清理环境; expect:成功
drop function if exists func_subpartition_0172();
drop function if exists func_subpartition_0172_01();
drop function if exists func_tri_subpartition_0172() cascade;
drop function if exists pro_subpartition_0172();
drop table if exists t_subpartition_0172;
drop tablespace if exists ts_subpartition_0172;