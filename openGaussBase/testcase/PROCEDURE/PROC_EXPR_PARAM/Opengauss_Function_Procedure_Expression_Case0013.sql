-- @testpoint: 表达式做为参数的存储过程测试--字符串处理函数-concat(str1,str2)

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_EXPR_PARAM_013(P1 CHAR,P2 VARCHAR,T1 OUT VARCHAR)  AS
BEGIN
T1:=CONCAT(P1,P2);
raise info 'T1=:%',T1;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/
--调用存储过程
DECLARE
V1 CHAR(100) :='P1iifhlgtyugbihvnjkvhkkend';
V2 VARCHAR(200) :='P2字符串@￥%……gjhvjhvgbhjcvyugiohASDF';
V3 VARCHAR2(300) ;
BEGIN
PROC_EXPR_PARAM_013(V1,V2,V3);
END;
/
--清理环境
drop PROCEDURE PROC_EXPR_PARAM_013;