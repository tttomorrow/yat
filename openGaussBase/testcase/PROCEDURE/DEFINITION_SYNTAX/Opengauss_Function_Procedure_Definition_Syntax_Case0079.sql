-- @testpoint: 匿名块使用操作符 幂（指数运算

DROP TABLE IF EXISTS test_procedure_insert_0796;
create table test_procedure_insert_079 (id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_079 (SELECT 2.0^3.0 AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_079;
drop table test_procedure_insert_079;