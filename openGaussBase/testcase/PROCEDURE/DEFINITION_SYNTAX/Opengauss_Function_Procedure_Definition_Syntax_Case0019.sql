-- @testpoint: 存储过程声明语法 定义变量 BOOL 并进行加减运算

--创建存储过程
DROP PROCEDURE if exists Proc_Syntax_019;
CREATE OR REPLACE PROCEDURE Proc_Syntax_019()
IS
DECLARE
emp_id  BOOL := false;
begin
emp_id := false+2;
raise info ':%',emp_id;
end;
/

--调用存储过程
call Proc_Syntax_019();

--清理环境
DROP PROCEDURE Proc_Syntax_019;