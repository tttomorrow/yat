-- @testpoint: 表达式做为参数的存储过程测试--字符串处理函数-current_timestamp()

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_EXPR_PARAM_019(P1 timestamp)  AS
BEGIN
raise info 'P1=:%',P1;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/
--调用存储过程
DECLARE
V1 timestamp:=current_timestamp(3);
BEGIN
PROC_EXPR_PARAM_019(V1);
END;
/
--调用存储过程
DECLARE
V2 timestamp:=current_timestamp(1);
BEGIN
PROC_EXPR_PARAM_019(V2);
END;
/
--清理环境
drop PROCEDURE PROC_EXPR_PARAM_019;