-- @testpoint: lpad中string长度>length
drop table if exists TEST_LPAD16;
create table TEST_LPAD16 (COL1 VARCHAR2(20),COL2 integer,COL3 VARCHAR2(20));
insert into TEST_LPAD16 values('123', 10, 'abc');
SELECT lpad(COL1,length(trim(COL1))-1,COL3) as RESULT from TEST_LPAD16;
drop table TEST_LPAD16;
