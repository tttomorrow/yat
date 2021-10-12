-- @testpoint: 存储过程声明语法 定义变量 CHAR(4000), 合理报错

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_017()
IS
DECLARE
emp_id  CHAR(4000) := 'dbcd'
begin
emp_id := 'dbcd';
raise info ':%',emp_id;
end;
/

--调用存储过程
call Proc_Syntax_017();

--清理环境
DROP PROCEDURE Proc_Syntax_017;