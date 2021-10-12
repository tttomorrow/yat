-- @testpoint: 测试存储过程中if判断的条件为bool类型的变量

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_004
AS 
  v_bool boolean;
begin
    select true into v_bool from sys_dummy;
    if(v_bool)
    then
       raise info 'The condition is true';
    end if;
end ;
/
--调用存储过程
Call PROC_IF_ELSE_004();

--清理环境
drop PROCEDURE PROC_IF_ELSE_004;