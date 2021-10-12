-- @testpoint: 自定义函数循环调用———层循环

--创建自定义函数
create or replace function func_loop_transfer_001(v_id int) return int is
  v_num bigint;
begin
  v_num:=power(v_id,2);
  return(v_num);
end ;
/
--匿名块中调用自定义函数
declare
  v_result bigint;
begin
  for i in 1 .. 9 loop
    select func_loop_transfer_001(i) into v_result;
    raise info 'v_result=%',v_result;
  end loop;
end;
/
--恢复环境
drop function if exists func_loop_transfer_001;

