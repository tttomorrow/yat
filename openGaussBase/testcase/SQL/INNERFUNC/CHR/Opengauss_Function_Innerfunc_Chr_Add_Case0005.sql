-- @testpoint: 参数为''、null及0
drop table if exists TEST_CHR13;
create table TEST_CHR13(COL integer);
insert into TEST_CHR13 values(null); 
select chr(COL) as RESULT from TEST_CHR13;
drop table TEST_CHR13;

drop table if exists TEST_CHR14;
create table TEST_CHR14(COL integer);
insert into TEST_CHR14 values('');
select chr(COL) as RESULT from TEST_CHR14;
drop table TEST_CHR14;

drop table if exists TEST_CHR1;
create table TEST_CHR1(COL integer);
insert into TEST_CHR1 values(0);
select chr(COL) as RESULT from TEST_CHR1;
drop table  TEST_CHR1;
