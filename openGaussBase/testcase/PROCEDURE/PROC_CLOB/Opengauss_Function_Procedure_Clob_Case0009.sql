-- @testpoint: 存储过程clob数据类型的测试,结合to_char函数

--创建存储过程
create or replace procedure proc_clob_009(p1 in clob) is
begin
    raise info 'result:%',p1;
    exception
    when no_data_found then
        raise info 'no_data_found';
end;
/
--调用存储过程
call proc_clob_009(to_char(88877));

call proc_clob_009(to_char(1234567890,'099999999999999'));

--删除存储过程
drop procedure proc_clob_009;

