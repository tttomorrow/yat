-- @testpoint: 标量类型%rowtype的测试———基本类型测试

--test procedure
--标量类型%type的测试———基本类型测试

drop table if exists FVT_PROC_SCALAR_ROWTYPE_table_008;
CREATE TABLE FVT_PROC_SCALAR_ROWTYPE_table_008(
  T1 INT NOT NULL,
  T2 INTEGER,
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

create unique index  FVT_PROC_SCALAR_ROWTYPE_table_index_008 on FVT_PROC_SCALAR_ROWTYPE_table_008(T1);
create index FVT_PROC_SCALAR_ROWTYPE_table_index1_008 on FVT_PROC_SCALAR_ROWTYPE_table_008(T2,T17,T20);

INSERT INTO FVT_PROC_SCALAR_ROWTYPE_table_008 VALUES(14,58813,546223078,1234567.78,12345.5678,12.2345678,1234.67,2345.78,12345.5678,12.2345678,12.44,'dbce',
'FFFF','abcdeg','ac','ade',123.46,'2012-08-08','2000-02-01 15:22:21.11','2012-02-01 15:12:11.32',false);
commit;

--创建存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_ROWTYPE_008(P1 INT)  AS
V1 FVT_PROC_SCALAR_ROWTYPE_table_008%rowtype;
BEGIN
select * into V1 from FVT_PROC_SCALAR_ROWTYPE_table_008 where T1=P1;
raise info 'T2=:%',V1.T2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_ROWTYPE_008(14);

--修改列属性
update FVT_PROC_SCALAR_ROWTYPE_table_008 set T2=null;
alter table FVT_PROC_SCALAR_ROWTYPE_table_008 modify T2 CHAR(200);
update FVT_PROC_SCALAR_ROWTYPE_table_008 set T2='this is a string';


--重新编译存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_ROWTYPE_008(P1 INT)  AS
V1 FVT_PROC_SCALAR_ROWTYPE_table_008%rowtype;
BEGIN
select * into V1 from FVT_PROC_SCALAR_ROWTYPE_table_008 where T1=P1;
raise info 'T2=:%',V1.T2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_ROWTYPE_008(14);

--恢复环境
drop table if exists FVT_PROC_SCALAR_ROWTYPE_table_008;
drop procedure if exists FVT_PROC_SCALAR_ROWTYPE_008;