-- @testpoint: 标量类型%type的测试———列属性改变



--test procedure
--标量类型%type的测试———列属性改变

drop table if exists FVT_PROC_SCALAR_TYPE_table_003;
CREATE TABLE FVT_PROC_SCALAR_TYPE_table_003(
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

create unique index  FVT_PROC_SCALAR_TYPE_table_index_003 on FVT_PROC_SCALAR_TYPE_table_003(T1);
create index FVT_PROC_SCALAR_TYPE_table_index1_003 on FVT_PROC_SCALAR_TYPE_table_003(T2,T17,T20);


--创建存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_TYPE_003()  AS
V1 FVT_PROC_SCALAR_TYPE_table_003.T3%type;
V2 FVT_PROC_SCALAR_TYPE_table_003.T3%type;
BEGIN
  select T3 into V1 from FVT_PROC_SCALAR_TYPE_table_003 where T1=12;
  V2:= V1+5;
    raise info 'V1=:%',V1;
    raise info 'V2=:%',V2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_TYPE_003();


--修改列属性
alter table FVT_PROC_SCALAR_TYPE_table_003 add T23 INT;--增加临时列
update FVT_PROC_SCALAR_TYPE_table_003 set T23=T3 ,T3=null;--把数据放到临时列，置空数据列

alter table FVT_PROC_SCALAR_TYPE_table_003 modify T3 INT;--修改字段类型
update FVT_PROC_SCALAR_TYPE_table_003 set T3=T23 where T23 is not null;--放回数据

alter table FVT_PROC_SCALAR_TYPE_table_003 drop column T23;--删除临时列

--重新编译存储过程
CREATE OR REPLACE PROCEDURE FVT_PROC_SCALAR_TYPE_003()  AS
V1 FVT_PROC_SCALAR_TYPE_table_003.T3%type;
V2 FVT_PROC_SCALAR_TYPE_table_003.T3%type;
BEGIN
  select T3 into V1 from FVT_PROC_SCALAR_TYPE_table_003 where T1=12;
  V2:= V1;
  raise info 'V1=:%',V1;
  raise info 'V2=:%',V2;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
END;
/

--调用存储过程
CALL FVT_PROC_SCALAR_TYPE_003();

--恢复环境
drop table if exists FVT_PROC_SCALAR_TYPE_table_003;
drop procedure if exists FVT_PROC_SCALAR_TYPE_003;
