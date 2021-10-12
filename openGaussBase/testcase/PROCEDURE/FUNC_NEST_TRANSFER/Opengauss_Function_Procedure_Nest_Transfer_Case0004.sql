-- @testpoint: 自定义函数嵌套调用———自定义函数嵌套存储过程

--创建带入参和出参的存储过程
create or replace procedure proc_nest_transfer_004(p1 varchar2,p2 out varchar2)
is
begin
  p2 := upper(p1);
  exception
  when no_data_found
  then
  raise info 'no_data_found';
end;
/
--创建自定义函数
create or replace function func_nest_transfer_004(p1 in varchar) return varchar2 is
  v_string varchar2(1000);
begin
  begin
   proc_nest_transfer_004(p1,v_string);
  end;
  return(v_string);
end;
/
--调用自定义函数
select func_nest_transfer_004('asfghaagghh字符串1123454%……&009#￥');

--恢复环境
drop function if exists func_nest_transfer_004;
drop procedure if exists proc_nest_transfer_004;
