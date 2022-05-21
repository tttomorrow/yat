-- @testpoint: listagg函数异常校验，合理报错
drop table if exists emp;
create table emp(deptno smallint,
eid bigint,
mgrno integer,
ename text,
job text,
bonus real,
hiredate timestamp without time zone,
vacationTime interval,
salary double precision,
entry date,
respite numeric);
insert into emp values(10,1,7782,'Mary','Developer','3000.12','1982-01-23 00:00:00','2 mons 10 days','200000.56','1982-01-22','90.2');
insert into emp values(10,2,7888,'Tony','Developer','4000.00','1981-09-08 00:00:00','4 days 06:00:00','20560.56','1981-09-07','7.2');
-- 多参、少参、非法入参
SELECT  deptno, listagg(job,job, '/') WITHIN GROUP(ORDER BY job) AS Work_Type FROM emp GROUP BY deptno;
SELECT  deptno, listagg() WITHIN GROUP(ORDER BY job) AS Work_Type FROM emp GROUP BY deptno;
SELECT  deptno, listagg(job,1-1>1) WITHIN GROUP(ORDER BY job) AS Work_Type FROM emp GROUP BY deptno;
select listagg(19223372036854775807::bigint) within group(order by 1) from sys_dummy;
drop table emp cascade;