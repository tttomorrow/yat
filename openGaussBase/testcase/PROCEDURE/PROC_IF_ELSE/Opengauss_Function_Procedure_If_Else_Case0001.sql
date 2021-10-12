-- @testpoint: 测试存储过程中if判断的关键字为True

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_001
AS 
begin
    if(TRue)
    then
       raise info 'The condition is true';
    end if;
end;
/
--调用存储过程
Call PROC_IF_ELSE_001();

--清理环境
drop PROCEDURE PROC_IF_ELSE_001;
