-- @testpoint:在匿名块中执行子查询的update语句

DROP TABLE IF EXISTS test_procedure_insert_01;
create table test_procedure_insert_01 (f1 int, f2 int);
insert into test_procedure_insert_01 values(1,2);

DROP TABLE IF EXISTS test_procedure_insert_02;
create table test_procedure_insert_02 (f1 int, f2 int);
insert into test_procedure_insert_02 values(1,999);

declare
v_sql varchar(1024);
begin
v_sql := 'Update test_procedure_insert_01 t1 set f2 = (select f2 from test_procedure_insert_02 t2 where t1.f1 = t2.f1)';
execute immediate v_sql;
raise info ':%',v_sql;
end;
/

select * from test_procedure_insert_01;
DROP TABLE test_procedure_insert_01;
DROP TABLE test_procedure_insert_02;