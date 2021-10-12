-- @testpoint: 测试execute immediate using子句是否支持常量入参（验证select中有using字句常量入参）

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

create or replace procedure TEST_PROC_USING_003 
AS
v_sql varchar2(2000);
BEGIN
    v_sql:='select * from TEST_EMP_001 where EMPNO = :v1 and EMPNAME = :v2 and JOB  = :v3';
    EXECUTE IMMEDIATE v_sql USING '8001', 'Kimy', 'MANAGER';	
END;
/

Call TEST_PROC_USING_003();
select * from TEST_EMP_001;
drop procedure TEST_PROC_USING_003;
drop table TEST_EMP_001;