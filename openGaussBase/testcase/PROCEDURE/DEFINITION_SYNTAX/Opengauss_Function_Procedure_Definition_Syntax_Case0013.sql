-- @testpoint: 存储过程声明语法 定义变量 BINARY_DOUBLE

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_013()
IS
DECLARE
emp_id  BINARY_DOUBLE := 1234.56;
begin
emp_id := 1234.56*2;
raise info ':%',emp_id;
end;
/

--调用存储过程
call Proc_Syntax_013();

--清理环境
DROP PROCEDURE Proc_Syntax_013;