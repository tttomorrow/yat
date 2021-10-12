-- @testpoint: 表达式做为参数的存储过程测试——字符串处理函数-LENGTH(),LENGTHB()

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_EXPR_PARAM_014(P1 CHAR,P2 VARCHAR,T1 OUT INT,T2 OUT BIGINT,T3 OUT INT,T4 OUT INT)  AS
BEGIN
T1:=LENGTH(P1);
raise info 'T1=:%',T1;
T2:=LENGTH(P2);
raise info 'T2=:%',T2;
T3:=LENGTHB(P1);
raise info 'T3=:%',T3;
T4:=LENGTHB(P2);
raise info'T4=:%',T4;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/
--调用存储过程
DECLARE
V1 CHAR(100) :='P1iifhlgtyugbihvnjkvhkkend';
V2 VARCHAR(200) :='P2字符串@￥%……gjhvjhvgbhjcvyugiohASDF';
V3 INT; 
V4 BIGINT;     
V5 INT; 
V6 INTEGER;
BEGIN
PROC_EXPR_PARAM_014(V1,V2,V3,V4,V5,V6);
END;
/
--清理环境
drop PROCEDURE PROC_EXPR_PARAM_014;
