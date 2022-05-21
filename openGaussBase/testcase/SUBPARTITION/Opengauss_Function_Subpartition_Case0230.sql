-- @testpoint: range_list二级分区表：触发器/函数/存储过程/游标

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0230;
drop tablespace if exists ts_subpartition_0230;
create tablespace ts_subpartition_0230 relative location 'subpartition_tablespace/subpartition_tablespace_0230';

--test1: 触发器
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0230
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0230
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
--step3: 创建函数,删除更新表数据; expect:成功
drop function if exists func_tri_subpartition_0230() cascade;
create or replace function func_tri_subpartition_0230() returns trigger as
           $$
           declare
           begin
                   delete from t_subpartition_0230; 
                   update t_subpartition_0230 set col_2 =10 where col_2=1;
                   return new;
           end
           $$ language plpgsql;
           /
--step4: 创建触发器,与二级分区表关联,执行插入语句时后执行函数; expect:成功
create trigger tri_subpartition_0230
          after insert on t_subpartition_0230
          for each row
          execute procedure func_tri_subpartition_0230();
          /
--step5: 插入数据; expect:成功
insert into t_subpartition_0230 values(1,1,1,1);
--step6: 查询表数据; expect:成功,无数据
select * from t_subpartition_0230;
--step7: 插入数据; expect:成功
insert into t_subpartition_0230 values(1,1,1,1);
--step8: 查询表数据; expect:成功,无数据
select * from t_subpartition_0230;
--step9: 插入数据; expect:成功
insert into t_subpartition_0230 values(2,2,2,2);
--step10: 查询数据; expect:成功,无数据
select * from t_subpartition_0230;
--step11: 删除函数; expect:成功
drop function if exists func_tri_subpartition_0230() cascade;

--test2: 函数
--step12: 清空表数据; expect:成功
truncate t_subpartition_0230;
--step13: 创建函数,返回boolean值; expect:成功
drop function if exists func_subpartition_0230() cascade;
create or replace function func_subpartition_0230() returns boolean as
    $$
    declare
    begin
         delete from t_subpartition_0230 where col_2=8;
         return 1;
    end
    $$ language plpgsql;
    /
--step14: 创建函数,删除指定条件的数据,无返回值; expect:成功
drop function if exists func_subpartition_0230() cascade;
create or replace function func_subpartition_0230() returns void as
    $$
    declare
    begin
         delete from t_subpartition_0230 where col_2=8;
    end
    $$ language plpgsql;
    /
--step15: 创建函数,有返回值; expect:成功
drop function if exists func_subpartition_0230_01() cascade;
create or replace  function func_subpartition_0230_01()
returns table(col_1 int,col_2 int,col_3 varchar2 ( 30 ) ,col_4 int) as $$
begin
     return query select * from t_subpartition_0230;
end;
$$ language plpgsql;
/

--step16: 插入数据; expect:成功
insert into t_subpartition_0230 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step17: 调用函数; expect:成功,无数据
call func_subpartition_0230();
--step18: 调用函数; expect:成功,4条数据
call func_subpartition_0230_01();

--test3: 存储过程
--step19: 创建存储过程,删除指定数据; expect:成功
drop function if exists pro_subpartition_0230();
create or replace procedure pro_subpartition_0230 is
    begin
         delete from t_subpartition_0230 where col_2=8;
    end;
    /
--step20: 清空表数据; expect:成功
truncate t_subpartition_0230;
--step21: 插入5条数据; expect:成功
insert into t_subpartition_0230 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step22: 调用存储过程; expect:成功
call  pro_subpartition_0230();
--step23: 查询数据; expect:成功,4条数据
select * from t_subpartition_0230;

--step24: 创建存储过程,输出多个变量; expect:成功
drop function if exists pro_subpartition_0230();
create or replace procedure pro_subpartition_0230(var out int,var1 out int) as
begin
  select col_1,col_2 into var,var1 from t_subpartition_0230 limit 1;
end;
/
--step25: 调用存储过程; expect:成功,有数据
call pro_subpartition_0230(1,2);


--test4: 游标
--step26: 清空表数据; expect:成功
truncate t_subpartition_0230;
--step27: 插入数据; expect:成功
insert into t_subpartition_0230 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0230 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);
--step28: 开启事务创建游标; expect:成功
begin;
cursor c1 for select * from t_subpartition_0230 subpartition (p_list_2_2);
fetch c1;
fetch c1;
fetch c1;
end;
/

--step29: 插入数据; expect:成功
insert into t_subpartition_0230 values (generate_series(-19, 50),generate_series(0, 60,10),generate_series(0, 99));
--step30: 创建package; expect:成功
drop package if exists pck0;
create or replace package pck0 as
    c1 int := 55;
    c2 int := 100;
    procedure proc1();
end pck0;
/
drop package if exists pck1;
create or replace package pck1 as
procedure proc1();
end pck1;
/
create or replace package body pck1 as
procedure proc1() as
  type csr is ref cursor;
  v_cur csr;
  v_sql varchar2;
  v_tbname varchar2 := 't_subpartition_0230';
  type t1 is varray(10) of int;
  var3 t1 := t1();
begin
  v_sql := 'select col_2 from ' || v_tbname || ' subpartition(p_range_5_subpartdefault1) where col_2 between :var1 and :var2';
  open v_cur for v_sql using public.pck0.c1, public.pck0.c2;
  loop
    fetch v_cur into var3(1);
    exit when v_cur%notfound;
    raise info 'var3(1) is %',var3(1);

  end loop;
end;
end pck1;
/
--step31: 调用存储过程; expect:成功
call pck1.proc1();

--step32: 清理环境; expect:成功
drop package if exists pck0;
drop package if exists pck1;
drop function if exists func_subpartition_0230();
drop function if exists func_subpartition_0230_01();
drop function if exists func_tri_subpartition_0230() cascade;
drop function if exists pro_subpartition_0230();
drop table if exists t_subpartition_0230;
drop tablespace if exists ts_subpartition_0230;