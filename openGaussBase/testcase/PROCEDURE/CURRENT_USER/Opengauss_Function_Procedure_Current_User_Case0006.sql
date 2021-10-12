-- @testpoint: 创建存储过程时带stable参数

--不带immutable创建存储过程
create or replace procedure test_proc_using_006(a int) as
declare
  v_lang clob := '你好';
begin
  for i in 1 .. 2 loop
    v_lang := v_lang || '你也好';
  end loop;
  raise notice '%',v_lang;
end;
/
call test_proc_using_006(22);
drop procedure test_proc_using_006;

--带immutable创建存储过程
create or replace procedure test_proc_using_006(a int) stable as
declare
  v_lang clob := '你好';
begin
  for i in 1 .. 2 loop
    v_lang := v_lang || '你也好';
  end loop;
  raise notice '%',v_lang;
end;
/
call test_proc_using_006(22);
drop procedure test_proc_using_006;