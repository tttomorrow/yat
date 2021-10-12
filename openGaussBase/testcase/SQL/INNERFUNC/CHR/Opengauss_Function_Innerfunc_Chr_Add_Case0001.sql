-- @testpoint: 有效值
drop table if exists TEST_CHR2;
create table TEST_CHR2(COL integer);
insert into TEST_CHR2 values(1);
select chr(COL) as RESULT from TEST_CHR2;
drop table TEST_CHR2;

drop table if exists TEST_CHR3;
create table TEST_CHR3(COL integer);
insert into TEST_CHR3 values(9);
select chr(COL) as RESULT from TEST_CHR3;
drop table TEST_CHR3;

drop table if exists TEST_CHR4;
create table TEST_CHR4(COL integer);
insert into TEST_CHR4 values(10);
select chr(COL) as RESULT from TEST_CHR4;
drop table TEST_CHR4;

drop table if exists TEST_CHR5;
create table TEST_CHR5(COL integer);
insert into TEST_CHR5 values(11);
select chr(COL) as RESULT from TEST_CHR5;
UPDATE TEST_CHR5 SET COL= 12;
select chr(COL) as RESULT from TEST_CHR5;
drop table TEST_CHR5;

drop table if exists TEST_CHR6;
create table TEST_CHR6(COL integer);
insert into TEST_CHR6 values(13);
select chr(COL) as RESULT from TEST_CHR6;
drop table TEST_CHR6;

drop table if exists TEST_CHR7;
create table TEST_CHR7(COL integer);
insert into TEST_CHR7 values(40);
select chr(COL) as RESULT from TEST_CHR7;
drop table TEST_CHR7;

drop table if exists TEST_CHR8;
create table TEST_CHR8(COL integer);
insert into TEST_CHR8 values(48);
select chr(COL) as RESULT from TEST_CHR8;
drop table TEST_CHR8;

drop table if exists TEST_CHR9;
create table TEST_CHR9(COL integer);
insert into TEST_CHR9 values(65);
insert into TEST_CHR9 values(78);
insert into TEST_CHR9 values(90);
select chr(COL) as RESULT from TEST_CHR9 order by RESULT;
drop table TEST_CHR9;

drop table if exists TEST_CHR10;
create table TEST_CHR10(COL integer);
insert into TEST_CHR10 values(94);
select chr(COL) as RESULT from TEST_CHR10;
drop table TEST_CHR10;

drop table if exists TEST_CHR11;
create table TEST_CHR11(COL integer);
insert into TEST_CHR11 values(97);
insert into TEST_CHR11 values(116);
insert into TEST_CHR11 values(122);
select chr(COL) as RESULT from TEST_CHR11 order by RESULT;
drop table TEST_CHR11;
