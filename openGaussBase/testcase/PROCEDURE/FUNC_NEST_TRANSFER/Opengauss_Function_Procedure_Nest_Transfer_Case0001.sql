-- @testpoint: 自定义函数嵌套调用———2层嵌套

--创建自定义函数1
create or replace function func_nest_transfer_001(v_id int) return int is
  v_num int;
  v_num1 int;
begin
  raise info 'func_nest_transfer_001 begin';
  v_num:=v_id+1;
  select func_nest_transfer_002(v_num) into v_num1 ;
  raise info'func_nest_transfer_001 end';
  return(v_num1);
end ;
/
--创建自定义函数2
create or replace function func_nest_transfer_002(v_id int) return int is
  v_num int;
begin
   raise info 'func_nest_transfer_002 begin';
  v_num:=v_id+1;
     raise info 'func_nest_transfer_002 end';
  return(v_num);
end ;
/
--调用自定义函数
select func_nest_transfer_001(3);

--恢复环境
drop function if exists func_nest_transfer_001;
drop function if exists func_nest_transfer_002;

