-- @testpoint: 表达式做为参数的存储过程测试--简单表达式-算数运算表达式，表达式在定义存储过程时作为参数

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_EXPR_PARAM_002(P1 INT :=1+3)  AS
BEGIN
raise info 'P1=:%',P1;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/
--调用存储过程
CALL PROC_EXPR_PARAM_002();
--清理环境
drop PROCEDURE PROC_EXPR_PARAM_002;