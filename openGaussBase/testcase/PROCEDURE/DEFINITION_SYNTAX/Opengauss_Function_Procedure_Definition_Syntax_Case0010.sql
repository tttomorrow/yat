-- @testpoint: 存储过程声明语法 定义变量 NUMBER(12,2)

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_010(IN name1 varchar2(20))
IS
DECLARE
emp_id  NUMBER(12,2) := 1234567.89;
begin
emp_id := 1234567.89+1;
raise info ':%',emp_id;
end;
/

--调用存储过程
call Proc_Syntax_010('V_name1');

--清理环境
DROP PROCEDURE Proc_Syntax_010;

