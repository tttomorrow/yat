-- @testpoint: listagg函数分隔符是中文、特殊字符等
drop table if exists emp;
create table emp(deptno smallint,
eid bigint,
mgrno integer,
ename text,
job text);
insert into emp values(10,1,7782,'Mary','Developer');
insert into emp values(10,2,7888,'Tony','Developer');
SELECT listagg(job, lpad(' # ',256,'@&')) WITHIN GROUP(ORDER BY job) AS result FROM emp;
SELECT listagg(job, '开发工程师') WITHIN GROUP(ORDER BY job) AS result FROM emp;
SELECT listagg(job, '/*&……%#@') WITHIN GROUP(ORDER BY job) AS result FROM emp;
drop table emp cascade;