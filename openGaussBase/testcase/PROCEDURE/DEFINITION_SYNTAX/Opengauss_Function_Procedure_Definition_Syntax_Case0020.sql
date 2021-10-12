-- @testpoint: 存储过程声明语法 定义变量 BOOL 并进行加减运算


--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_020()
IS
DECLARE
emp_id  BOOL := false;
begin
emp_id := false+true;
raise info ':%',emp_id;
end;
/

--调用存储过程
call Proc_Syntax_020();

--清理环境
DROP PROCEDURE Proc_Syntax_020;