-- @testpoint: 存储过程clob数据类型的测试,测试clob类型为空

--创建存储过程
create or replace procedure proc_clob_001() is
v1 clob;
begin
    if v1 is null then
        raise info 'v1 is null';
    else
        raise info 'v1 is not null';
    end if;
end;
/
--调用存储过程
call proc_clob_001();

--恢复环境
drop procedure if exists proc_clob_001;
