-- @testpoint: 存储过程clob数据类型的测试,测试传入非字符串类型

--创建存储过程
create or replace procedure proc_clob_008(p1 in clob) is
begin
  raise info 'result:%',p1;
  exception
when no_data_found then raise info 'no_data_found';
end;
/
--调用存储过程
call proc_clob_008(12);
call proc_clob_008(12.256);
call proc_clob_008(date'0001-01-01 00:00:00');

--恢复环境
drop procedure proc_clob_008;

