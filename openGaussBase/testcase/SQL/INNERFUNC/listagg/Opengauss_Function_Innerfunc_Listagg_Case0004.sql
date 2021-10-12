-- @testpoint: listagg函数聚集列类型是时间类型
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
insert into emp values(20,3,7342,'Hebe','Product','1000.34','1997-09-28 00:00:00','10 days','29750.56','1997-09-27','30.2');
insert into emp values(20,4,7212,'Tom','Manager','3050.82','2010-02-22 00:00:00','3 mons','15760.56','2010-02-21','307.2');
insert into emp values(30,5,7002,'John','Testing','9000.12','2015-02-20 00:00:00','2 mons 30 days','20000.56','2015-02-19','999');
insert into emp values(30,6,7992,'Jack','it','2000.89','1999-12-17 00:00:00','1 year 1 mon','700000.56','1999-12-16','30.99');
SELECT deptno, listagg(hiredate, ', ') WITHIN GROUP(ORDER BY hiredate DESC) AS hiredates FROM emp GROUP BY deptno;
SELECT ename, listagg(entry, '  ||  ') WITHIN GROUP(ORDER BY entry DESC) AS comein FROM emp GROUP BY ename;
drop table emp cascade;