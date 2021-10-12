-- @testpoint: 存储过程clob数据类型的测试,测试clob类型作为存储过程的in out类型参数,和字符串处理函数substr结合

--创建存储过程
create or replace procedure proc_clob_007(p1 in out clob) is
begin
  raise info 'old length=:%',char_length(p1);
  p1 := substr(p1,1000);
  raise info 'new length=:%',char_length(p1);
  exception
when no_data_found then raise info 'no_data_found';
end;
/
--调用存储过程
declare
  v1 text :='';
begin
  for i in 1 .. 1000 loop
    v1:= v1||'这是一个clob类型';
  end loop;
  proc_clob_007(v1);
end;
/
--恢复环境
drop procedure if exists proc_clob_007;
