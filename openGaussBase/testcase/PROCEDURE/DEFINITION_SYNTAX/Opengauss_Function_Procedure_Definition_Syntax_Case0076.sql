-- @testpoint:  匿名块使用操作符 除法 /

DROP TABLE IF EXISTS test_procedure_insert_076;
create table test_procedure_insert_076 (id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_076 (SELECT 4/2 AS RESULT, 3)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_076;
drop table test_procedure_insert_076;
