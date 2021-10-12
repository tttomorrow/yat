-- @testpoint: 标量类型%type的测试———列属性改变



drop table if exists FVT_PROC_SCALAR_TYPE_table_009;
CREATE TABLE FVT_PROC_SCALAR_TYPE_table_009(
  T1 INT,
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

create unique index  FVT_PROC_SCALAR_TYPE_table_index_009 on FVT_PROC_SCALAR_TYPE_table_009(T1);
create index FVT_PROC_SCALAR_TYPE_table_index1_009 on FVT_PROC_SCALAR_TYPE_table_009(T2,T17,T20);
commit;

--创建存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_TYPE_009()  AS
V1 FVT_PROC_SCALAR_TYPE_table_009.T11%type;
V2 FVT_PROC_SCALAR_TYPE_table_009.T11%type;
BEGIN
  select T11 into V1 from FVT_PROC_SCALAR_TYPE_table_009 where T1=12;
  V2:= V1+12.3456789;
  raise info 'V1=:%',V1;
  raise info 'V2=:%',V2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_TYPE_009();


--修改列属性
alter table FVT_PROC_SCALAR_TYPE_table_009 add T23 DECIMAL(10,5);
update FVT_PROC_SCALAR_TYPE_table_009 set T23=T11 ,T11=null;
commit;
alter table FVT_PROC_SCALAR_TYPE_table_009 modify T11 DECIMAL(10,5);
update FVT_PROC_SCALAR_TYPE_table_009 set T11=T23 where T23 is not null;
commit;
alter table FVT_PROC_SCALAR_TYPE_table_009 drop column T23;

--重新编译存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_TYPE_009()  AS
V1 FVT_PROC_SCALAR_TYPE_table_009.T11%type;
V2 FVT_PROC_SCALAR_TYPE_table_009.T11%type;
BEGIN
  select T11 into V1 from FVT_PROC_SCALAR_TYPE_table_009 where T1=12;
  V2:= V1+12.3456789;
  raise info 'V1=:%',V1;
  raise info 'V2=:%',V2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/


--调用存储过程
CALL FVT_PROC_SCALAR_TYPE_009();

--恢复环境
drop table if exists FVT_PROC_SCALAR_TYPE_table_009;
drop procedure if exists FVT_PROC_SCALAR_TYPE_009;
