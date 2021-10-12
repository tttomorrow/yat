-- @testpoint: 标量类型%type的测试———基本类型测试




--test procedure
--标量类型%type的测试———基本类型测试

drop table if exists FVT_PROC_SCALAR_TYPE_table_001;
CREATE TABLE FVT_PROC_SCALAR_TYPE_table_001(
  T1 INT,
  T2 INTEGER NOT NULL,
  T3 BIGINT,
  T4 NUMBER DEFAULT 0.2332,
  T5 NUMBER(12,2),
  T6 NUMBER(12,6),
  T7 BINARY_DOUBLE,
  T8 DECIMAL,
  T9 DECIMAL(8,2),
  T10 DECIMAL(8,4),
  T11 REAL,
  T12 CHAR(4000),
  T13 CHAR(100),
  T14 VARCHAR(4000),
  T15 VARCHAR(100),
  T16 VARCHAR2(4000),
  T17 NUMERIC,

  T19 DATE,
  T20 TIMESTAMP,
  T21 TIMESTAMP(6),
  T22 BOOL
) ;

create unique index  FVT_PROC_SCALAR_TYPE_table_index_001 on FVT_PROC_SCALAR_TYPE_table_001(T1);
create index FVT_PROC_SCALAR_TYPE_table_index1_001 on FVT_PROC_SCALAR_TYPE_table_001(T2,T17,T20);



--创建存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_TYPE_001()  AS
V1 FVT_PROC_SCALAR_TYPE_table_001.T2%type;
V2 FVT_PROC_SCALAR_TYPE_table_001.T14%type;
BEGIN
select T2,T14 into V1,V2 from FVT_PROC_SCALAR_TYPE_table_001 where T1=15;
raise info 'V1=:%',V1;
raise info 'V2=:%',V2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_TYPE_001();

--恢复环境
drop table if exists FVT_PROC_SCALAR_TYPE_table_001;
drop procedure if exists FVT_PROC_SCALAR_TYPE_001;