-- @testpoint: lpad函数参数一三为可变长类型
drop table if exists TEST_LPAD16;
create table TEST_LPAD16 (COL1 VARCHAR2(20),COL2 integer,COL3 VARCHAR2(20));
insert into TEST_LPAD16 values('123', 10, 'abc');
SELECT lpad(COL1,COL2,COL3) as RESULT from TEST_LPAD16;
drop table TEST_LPAD16;
