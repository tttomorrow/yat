-- @testpoint: 有效值
drop table if exists TEST_CHR12;
create table TEST_CHR12(COL integer);
insert into TEST_CHR12 values(127);
select chr(COL) as RESULT from TEST_CHR12;
drop table TEST_CHR12;
