-- @testpoint: 存储过程结合二进制类型的测试 raw类型最大支持8000字节

--创建存储过程
create or replace procedure proc_binary_005() is
  v_lang raw(8000) := 'ffffffffff';
begin
    for i in 1 .. 799 loop
        v_lang := v_lang || 'ffffffffff';
    end loop;
        raise info 'v_lang=:%',v_lang;
        raise info 'length=:%',length(v_lang);
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/

--调用存储过程
call proc_binary_005();

--恢复环境
drop procedure if exists proc_binary_005;

