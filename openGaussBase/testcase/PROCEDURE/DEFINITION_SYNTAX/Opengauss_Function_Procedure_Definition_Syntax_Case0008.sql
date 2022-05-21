-- @testpoint: 存储过程声明语法带 定义变量 BIGINT

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_008(IN name1 varchar2(20))
IS
DECLARE
emp_id  BIGINT := 5462230555579;
begin
emp_id := 5462230555579+1;
raise info ':%',emp_id;
end;
/

--调用存储过程
call Proc_Syntax_008('李华');

--清理环境
DROP PROCEDURE  Proc_Syntax_008;
