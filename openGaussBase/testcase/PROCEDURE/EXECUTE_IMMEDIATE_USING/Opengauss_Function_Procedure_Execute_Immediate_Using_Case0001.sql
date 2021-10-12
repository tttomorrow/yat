-- @testpoint: 创建存储过程并测试execute immediate using子句是否支持常量入参

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

create or replace procedure TEST_PROC_USING_001(
  V_EMPNO    IN  TEST_EMP_001.EMPNO%TYPE,
  V_EMPNAME  IN  TEST_EMP_001.EMPNAME%TYPE
  ) AS
  v_sql VARCHAR2(2000);
BEGIN
    v_sql := 'insert into TEST_EMP_001 values (:v1,:v2,:v3,:v4,:v5,:v6,:v7)';
    EXECUTE IMMEDIATE v_sql USING '8001', 'Kimy', 'MANAGER','7839',to_date('1981-06-09','yyyy-mm-dd'),'2450','10';
	insert into TEST_EMP_001
	  (
		 EMPNO,
		 EMPNAME,
		 JOB
	  )
	  VALUES
	  (
		 V_EMPNO,
		 V_EMPNAME,
		 'MANAGER'
	  );
END;
/

call TEST_PROC_USING_001(10,12);
select * from TEST_EMP_001;
drop procedure TEST_PROC_USING_001;
drop table TEST_EMP_001;