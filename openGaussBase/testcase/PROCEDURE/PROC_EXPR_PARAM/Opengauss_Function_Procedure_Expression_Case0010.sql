-- @testpoint: 表达式做为参数的存储过程测试--函数表达式-LN()

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_EXPR_PARAM_010(P1 DECIMAL)  AS
BEGIN
raise info 'P1=:%',P1;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/
--调用存储过程
DECLARE
V1 DECIMAL :=LN(1);
V2 DECIMAL :=LN(2);
V3 DECIMAL :=LN(97);

BEGIN
 PROC_EXPR_PARAM_010(V1);
 PROC_EXPR_PARAM_010(V2);
 PROC_EXPR_PARAM_010(V3);
END;
/
--清理环境
drop PROCEDURE PROC_EXPR_PARAM_010;
