-- @testpoint:在匿名块中插入加括号select的语句

DROP TABLE IF EXISTS test_procedure_insert_01;
create table test_procedure_insert_01 (f1 int, f2 int);

declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_01 (select 1, 1 )';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_01;
DROP table test_procedure_insert_01;