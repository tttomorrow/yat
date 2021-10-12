-- @testpoint: insert语句中使用
drop table if exists test_avg_001;
create table test_avg_001(
COL_1 bigint,
COL_2 TIMESTAMP WITHOUT TIME ZONE,
COL_3 boolean,
COL_4 decimal,
COL_5 text,
COL_6 smallint,
COL_7 char(30),
COL_17 int ,
COL_42 number(6,2),
COL_44 varchar2(50),
COL_58 number(12,6));
1,'@dfsgdf',8,32.23,'gfhgfh',122);
drop table if exists test_avg_003;
create table test_avg_003(COL_AVG1 int,COL_AVG2 number(6,2),COL_AVG3 number(12,6));
insert into test_avg_003 select avg(COL_17),avg(COL_42),avg(COL_58) from test_avg_001;
commit;
select * from test_avg_003 order by 1,2,3;
drop table if exists test_avg_003;
drop table if exists test_avg_001;