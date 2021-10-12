-- @testpoint: 测试clob类型作为自定义函数的参数，和字符串处理函数substr结合

--创建自定义函数
create or replace function fvt_func_clob_006(p1 clob) return char
is
v_1 clob:='';
v_lang clob;
v_length int;
begin
  for i in 1 ..3  loop
    v_1:= v_1||p1;
  end loop;
    v_lang := substr(v_1,1,3);
    return v_lang;
  exception
  when no_data_found
  then
    raise info 'no_data_found';
end;
/
--调用自定义函数
select fvt_func_clob_006('clob');

--恢复环境
drop function if exists fvt_func_clob_006;