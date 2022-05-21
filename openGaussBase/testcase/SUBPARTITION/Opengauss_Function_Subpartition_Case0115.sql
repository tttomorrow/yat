-- @testpoint: list_range二级分区表：触发器/函数/存储过程/游标

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0115;
drop tablespace if exists ts_subpartition_0115;
create tablespace ts_subpartition_0115 relative location 'subpartition_tablespace/subpartition_tablespace_0115';

--test1: 触发器
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0115
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0115
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
--step3: 创建函数，删除更新表数据; expect:成功
drop function if exists func_tri_subpartition_0115() cascade;
create or replace function func_tri_subpartition_0115() returns trigger as
           $$
           declare
           begin
                   delete from t_subpartition_0115; 
                   update t_subpartition_0115 set col_2 =10 where col_2=1;
                   return new;
           end
           $$ language plpgsql;
           /
--step4: 创建触发器，与二级分区表关联，执行插入语句时后执行函数; expect:成功
create trigger tri_subpartition_0115
          after insert on t_subpartition_0115
          for each row
          execute procedure func_tri_subpartition_0115();
          /
--step5: 插入数据; expect:成功
insert into t_subpartition_0115 values(1,1,1,1);
--step6: 查询表数据; expect:成功，无数据
select * from t_subpartition_0115;
--step7: 插入数据; expect:成功
insert into t_subpartition_0115 values(1,1,1,1);
--step8: 查询表数据; expect:成功，无数据
select * from t_subpartition_0115;
--step9: 插入数据; expect:成功
insert into t_subpartition_0115 values(2,2,2,2);
--step10: 查询表数据; expect:成功，无数据
select * from t_subpartition_0115;
--step8: 删除函数; expect:成功
drop function if exists func_tri_subpartition_0115() cascade;

--test2: 函数
--step11: 清空表数据; expect:成功
truncate t_subpartition_0115;
--step12: 创建函数，返回boolean值; expect:成功
drop function if exists func_subpartition_0115() cascade;
create or replace function func_subpartition_0115() returns boolean as
    $$
    declare
    begin
         delete from t_subpartition_0115 where col_2=8;
         return 1;
    end
    $$ language plpgsql;
    /
--step13: 创建函数，删除指定条件的数据，无返回值; expect:成功
drop function if exists func_subpartition_0115() cascade;
create or replace function func_subpartition_0115() returns void as
    $$
    declare
    begin
         delete from t_subpartition_0115 where col_2=8;
    end
    $$ language plpgsql;
    /
--step14: 创建函数，有返回值; expect:成功
drop function if exists func_subpartition_0115_01() cascade;
create or replace  function func_subpartition_0115_01()
returns table(col_1 int,col_2 int,col_3 varchar2 ( 30 ) ,col_4 int) as $$
begin
     return query select * from t_subpartition_0115;
end;
$$ language plpgsql;
/

--step15: 插入5条数据; expect:成功
insert into t_subpartition_0115 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step16: 调用函数; expect:成功，无数据
call func_subpartition_0115();
--step17: 调用函数; expect:成功，4条数据
call func_subpartition_0115_01();

--test3: 存储过程
--step18: 创建存储过程，删除指定数据; expect:成功
drop function if exists pro_subpartition_0115();
create or replace procedure pro_subpartition_0115 is
    begin
         delete from t_subpartition_0115 where col_2=8;
    end;
    /
--step19: 清空表数据数据; expect:成功
truncate t_subpartition_0115;
--step20: 插入5条数据; expect:成功
insert into t_subpartition_0115 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step21: 调用存储过程; expect:成功
call  pro_subpartition_0115();
--step22: 查询数据; expect:成功，4条数据
select * from t_subpartition_0115;

--test4: 游标
--step23: 清空表数据数据; expect:成功
truncate t_subpartition_0115;
--step24: 插入数据; expect:成功
insert into t_subpartition_0115 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0115 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step25: 开启事务创建游标; expect:成功
begin;
cursor c1 for select * from t_subpartition_0115 subpartition (p_list_2_subpartdefault1);
fetch c1;
fetch c1;
fetch c1;
end;
/

--step26: 清理环境; expect:成功
drop function if exists func_subpartition_0115();
drop function if exists func_subpartition_0115_01();
drop function if exists func_tri_subpartition_0115() cascade;
drop function if exists pro_subpartition_0115();
drop table if exists t_subpartition_0115;
drop tablespace if exists ts_subpartition_0115;