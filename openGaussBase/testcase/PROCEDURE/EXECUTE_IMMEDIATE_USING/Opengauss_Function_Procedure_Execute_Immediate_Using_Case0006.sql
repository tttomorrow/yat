-- @testpoint: 测试execute immediate using子句是否支持常量入参（验证sing字句是否支持常量和变量混合入参）

DROP TABLE IF EXISTS TEST_EMP_001;
CREATE TABLE TEST_EMP_001
(
  EMPNO VARCHAR(20) NOT NULL ,
  EMPNAME VARCHAR(20),
  JOB VARCHAR(20),
  MGR INT,
  HIREDATE DATE,
  SALARY INT,
  DEPTNO INT
);

create or replace procedure TEST_PROC_USING_006(
  V_EMPNO    IN  TEST_EMP_001.EMPNO%TYPE,
  V_EMPNAME  IN  TEST_EMP_001.EMPNAME%TYPE
  ) AS
  V_EMPNO_01 VARCHAR(20);
  V_EMPNAME_01 VARCHAR(20);
  v_sql VARCHAR2(2000);
BEGIN
    V_EMPNO_01 :=V_EMPNO;
	V_EMPNAME_01 :=V_EMPNAME;
    v_sql := 'insert into TEST_EMP_001 values (:v1,:v2,:v3,:v4,:v5,:v6,:v7)';
    EXECUTE IMMEDIATE v_sql USING V_EMPNO_01,V_EMPNAME_01,'MANAGER','2656',to_date('1989-02-20','yyyy-mm-dd'),'3600','29';
END;
/

Call TEST_PROC_USING_006(10,12);
select * from TEST_EMP_001;
drop procedure TEST_PROC_USING_006;
drop table TEST_EMP_001;