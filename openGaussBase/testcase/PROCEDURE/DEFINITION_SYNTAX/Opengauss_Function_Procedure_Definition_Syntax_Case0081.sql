-- @testpoint: 匿名块使用操作符 ||/  立方根

DROP TABLE IF EXISTS test_procedure_insert_081;
create table test_procedure_insert_081 (id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_081 (SELECT ||/ 27.0 AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_081;
drop table test_procedure_insert_081;