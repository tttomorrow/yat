-- @testpoint: listagg函数分隔符缺省时，默认为空。
drop table if exists emp;
create table emp(deptno smallint,
eid bigint,
mgrno integer,
ename text);
insert into emp values(10,1,7782,'Mary');
insert into emp values(10,2,7888,'Tony');
insert into emp values(20,3,7342,'Hebe');
insert into emp values(20,4,7212,'Tom');
insert into emp values(30,5,7002,'John');
insert into emp values(30,6,7992,'Jack');
SELECT listagg(ename) WITHIN GROUP(ORDER BY ename) AS people FROM emp;
drop table emp cascade;