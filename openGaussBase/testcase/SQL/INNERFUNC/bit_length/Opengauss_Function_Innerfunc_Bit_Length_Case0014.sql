-- @testpoint: 参数为变量
drop table if exists TEST_LPAD16;
create table TEST_LPAD16 (COL1 VARCHAR2(20),COL2 integer,COL3 VARCHAR2(20));
insert into TEST_LPAD16 values('123', 10, 'abc');
select bit_length(COL1)from TEST_LPAD16;
drop table if exists TEST_LPAD16;
