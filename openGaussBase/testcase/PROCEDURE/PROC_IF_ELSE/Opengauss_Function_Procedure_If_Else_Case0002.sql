-- @testpoint: 测试存储过程中if判断的关键字为False

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_002
AS 
begin
    if(FAlse)
    then
        raise info 'The condition is true';
    else
        raise info 'The condition is false';
    end if;
end ;
/
--调用存储过程
Call PROC_IF_ELSE_002();

--清理环境
drop PROCEDURE PROC_IF_ELSE_002;