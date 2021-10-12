-- @testpoint: 自定义函数循环调用———内层循环

create table func_loop_transfer_table_002(id int,power bigint);

--创建自定义函数
create or replace function func_loop_transfer_002() return int is
  v_num bigint;
begin
  for i in 1 .. 99 loop
    insert into func_loop_transfer_table_002 values(i,power(i,2));
  end loop;
  select count(1) into v_num from func_loop_transfer_table_002;
  return(v_num);
end;
/

select count(id) from func_loop_transfer_table_002;
select func_loop_transfer_002();
select count(id) from func_loop_transfer_table_002;

--恢复环境
drop function if exists func_loop_transfer_002;
drop table if exists func_loop_transfer_table_002;

