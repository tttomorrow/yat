-- @testpoint: 标量类型%type的测试———列属性改变




--test procedure
--标量类型%type的测试———列属性改变

drop table if exists FVT_PROC_SCALAR_TYPE_table_005;
CREATE TABLE FVT_PROC_SCALAR_TYPE_table_005(
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
  T13 VARCHAR(1000),
  T14 VARCHAR(4000),
  T15 VARCHAR(100),
  T16 VARCHAR2(4000),
  T17 NUMERIC,

  T19 DATE,
  T20 TIMESTAMP,
  T21 TIMESTAMP(6),
  T22 BOOL
) ;

create unique index  FVT_PROC_SCALAR_TYPE_table_index_005 on FVT_PROC_SCALAR_TYPE_table_005(T1);
create index FVT_PROC_SCALAR_TYPE_table_index1_005 on FVT_PROC_SCALAR_TYPE_table_005(T2,T17,T20);
commit;

--创建存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_TYPE_005()  AS
V1 FVT_PROC_SCALAR_TYPE_table_005.T13%type;
V2 FVT_PROC_SCALAR_TYPE_table_005.T13%type;
BEGIN
  select T13 into V1 from FVT_PROC_SCALAR_TYPE_table_005 where T1=12;
  V2:= V1||'字符串';
    raise info 'V1=:%',V1;
    raise info 'V2=:%',V2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_TYPE_005();


--修改列属性
alter table FVT_PROC_SCALAR_TYPE_table_005 add T23 VARCHAR(100);--增加临时列
update FVT_PROC_SCALAR_TYPE_table_005 set T23=T13 ,T13=null;--把数据放到临时列，置空数据列

alter table FVT_PROC_SCALAR_TYPE_table_005 modify T13 INT;--修改字段类型
update FVT_PROC_SCALAR_TYPE_table_005 set T13=T23 where T23 is not null;--放回数据

alter table FVT_PROC_SCALAR_TYPE_table_005 drop column T23;--删除临时列

--重新编译存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_TYPE_005()  AS
V1 FVT_PROC_SCALAR_TYPE_table_005.T13%type;
V2 FVT_PROC_SCALAR_TYPE_table_005.T13%type;
BEGIN
  select T13 into V1 from FVT_PROC_SCALAR_TYPE_table_005 where T1=12;
  V2:= V1||'字符串';
  raise info 'V1=:%',V1;
  raise info 'V2=:%',V2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_TYPE_005();

--恢复环境
drop table if exists FVT_PROC_SCALAR_TYPE_table_005;
drop procedure if exists FVT_PROC_SCALAR_TYPE_005;
