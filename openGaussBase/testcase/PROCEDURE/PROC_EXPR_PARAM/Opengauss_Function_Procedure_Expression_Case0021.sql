-- @testpoint: 表达式做为参数的存储过程测试——类型转换-ASCII()

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_EXPR_PARAM_021(P1 CHAR,T1 OUT INT)  AS
BEGIN
T1:=ASCII(P1);
raise info 'T1=:%',T1;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/
--调用存储过程
DECLARE
V1 CHAR(64);
V2 INT :=ASCII(V1);
BEGIN
PROC_EXPR_PARAM_021(V1,V2);
END;
/
--调用存储过程
DECLARE
V3 CHAR(200) :='Qeuig23';
V4 INT :=ASCII(V3);
BEGIN
PROC_EXPR_PARAM_021(V3,V4);
END;
/
--清理环境
drop PROCEDURE PROC_EXPR_PARAM_021;