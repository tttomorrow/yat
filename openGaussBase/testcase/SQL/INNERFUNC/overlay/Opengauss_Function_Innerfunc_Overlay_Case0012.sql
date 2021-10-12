-- @testpoint: overlay函数参数为变长类型字符串
drop table if exists TEST_LPAD16;
create table TEST_LPAD16 (COL1 VARCHAR2(20),COL2 integer,COL3 VARCHAR2(20));
insert into TEST_LPAD16 values('jsgfkjs', 10, 'abc');
SELECT overlay(COL1 placing 'world' from 2 for 3 ) from test_lpad16;
drop table if exists TEST_LPAD16;
