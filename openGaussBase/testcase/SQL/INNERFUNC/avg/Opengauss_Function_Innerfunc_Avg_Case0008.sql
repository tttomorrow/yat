-- @testpoint: join条件

drop table if exists test_avg_004;
create table test_avg_004(f0 number(10,6), f1 int, f3 char(10), f4 varchar(10), f5 number(10,6));
insert into test_avg_004(f0, f1, f3, f4, f5) values(500.5, 2, '5', 'test', 87.223);
insert into test_avg_004(f0, f1, f3, f4, f5) values(500.5,1.112233,'3','nebulaisok',998.22222);

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

commit;
select  a.t1,a.t2,b.y2,b.y3 from (select avg(COL_17) t1,avg(COL_42) t2,avg(COL_58) t3 from test_avg_001) a 
inner join (select avg(f0) y1,avg(f1) y2,avg(f5) y3 from test_avg_004) b on a.t1=b.y1 order by 1,2,3,4;

drop table if exists test_avg_004;
drop table if exists test_avg_001;

