-- @testpoint: 测试execute immediate using子句是否支持常量入参（验证delete中有using字句是否支持常量入参）

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

create or replace procedure TEST_PROC_USING_005 
AS
v_sql varchar2(2000);
BEGIN
    v_sql:='delete from TEST_EMP_001 where EMPNO = :v1 and EMPNAME = :v2';
    EXECUTE IMMEDIATE v_sql USING '8001', 'Kimy';
END;
/

Call TEST_PROC_USING_005();
select * from TEST_EMP_001;
drop procedure TEST_PROC_USING_005;
drop table TEST_EMP_001;