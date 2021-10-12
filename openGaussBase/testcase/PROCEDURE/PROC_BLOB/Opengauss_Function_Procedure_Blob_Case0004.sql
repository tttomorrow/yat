-- @testpoint: 存储过程blob数据类型的测试,存储过程内的blob类型最大支持8000

--创建存储过程
create or replace procedure proc_blob_004() is
v_lang blob := '01011110';
v_temp int;
begin
    for i in 1 .. 7999 loop
        v_lang := v_lang || '0';
    end loop;
    select char_length(v_lang::raw) into v_temp;
    raise info 'v_temp=%',v_temp;
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/
--调用存储过程
call proc_blob_004();

--恢复环境
drop procedure proc_blob_004;



