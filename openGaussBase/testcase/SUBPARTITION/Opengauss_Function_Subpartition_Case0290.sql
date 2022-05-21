-- @testpoint: range_range二级分区表：触发器/函数/存储过程/游标

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0290;
drop tablespace if exists ts_subpartition_0290;
create tablespace ts_subpartition_0290 relative location 'subpartition_tablespace/subpartition_tablespace_0290';

--test1: 触发器
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0290
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0290
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
--step3: 创建函数,删除更新表数据; expect:成功
drop function if exists func_tri_subpartition_0290() cascade;
create or replace function func_tri_subpartition_0290() returns trigger as
           $$
           declare
           begin
                   delete from t_subpartition_0290;
                   update t_subpartition_0290 set col_2 =10 where col_2=1;
                   return new;
           end
           $$ language plpgsql;
           /
--step4: 创建触发器,与二级分区表关联,执行插入语句时后执行函数; expect:成功
create trigger tri_subpartition_0290
          after insert on t_subpartition_0290
          for each row
          execute procedure func_tri_subpartition_0290();
          /
--step5: 插入数据后查询表数据; expect:成功,表中无数据
insert into t_subpartition_0290 values(1,1,1,1);
select * from t_subpartition_0290;
--step6: 插入数据后查询表数据; expect:成功,表中无数据
insert into t_subpartition_0290 values(1,1,1,1);
select * from t_subpartition_0290;
insert into t_subpartition_0290 values(2,2,2,2);
select * from t_subpartition_0290;
--step7: 删除函数; expect:成功
drop function if exists func_tri_subpartition_0290() cascade;

--test2: 函数
--step8: 清空表数据; expect:成功
truncate t_subpartition_0290;
--step9: 创建函数,返回boolean值; expect:成功
drop function if exists func_subpartition_0290() cascade;
create or replace function func_subpartition_0290() returns boolean as
    $$
    declare
    begin
         delete from t_subpartition_0290 where col_2=8;
         return 1;
    end
    $$ language plpgsql;
    /
--step10: 创建函数,删除指定条件的数据,无返回值; expect:成功
drop function if exists func_subpartition_0290() cascade;
create or replace function func_subpartition_0290() returns void as
    $$
    declare
    begin
         delete from t_subpartition_0290 where col_2=8;
    end
    $$ language plpgsql;
    /
--step11: 创建函数,有返回值; expect:成功
drop function if exists func_subpartition_0290_01() cascade;
create or replace  function func_subpartition_0290_01()
returns table(col_1 int,col_2 int,col_3 varchar2 ( 30 ) ,col_4 int) as $$
begin
     return query select * from t_subpartition_0290;
end;
$$ language plpgsql;
/

--step12: 插入数据; expect:成功
insert into t_subpartition_0290 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step13: 调用函数; expect:成功,无数据
call func_subpartition_0290();
--step14: 调用函数; expect:成功,4条数据
call func_subpartition_0290_01();

--test3: 存储过程
--step15: 创建存储过程,删除指定数据; expect:成功
drop function if exists pro_subpartition_0290();
create or replace procedure pro_subpartition_0290 is
    begin
         delete from t_subpartition_0290 where col_2=8;
    end;
    /
--step16: 清空表数据; expect:成功
truncate t_subpartition_0290;
--step17: 插入数据; expect:成功
insert into t_subpartition_0290 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step18: 调用存储过程; expect:成功
call  pro_subpartition_0290();
--step19: 查询数据; expect:成功,4条数据
select * from t_subpartition_0290;

--test4: 游标
--step20: 清空表数据; expect:成功
truncate t_subpartition_0290;
--step21: 插入数据; expect:成功
insert into t_subpartition_0290 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0290 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step22: 开启事务创建游标; expect:成功
begin;
cursor c1 for select * from t_subpartition_0290 subpartition (p_range_1_2);
fetch c1;
fetch c1;
fetch c1;
end;
/

--step23: 清理环境; expect:成功
drop function if exists func_subpartition_0290();
drop function if exists func_subpartition_0290_01();
drop function if exists func_tri_subpartition_0290() cascade;
drop function if exists pro_subpartition_0290();
drop table if exists t_subpartition_0290;
drop tablespace if exists ts_subpartition_0290;