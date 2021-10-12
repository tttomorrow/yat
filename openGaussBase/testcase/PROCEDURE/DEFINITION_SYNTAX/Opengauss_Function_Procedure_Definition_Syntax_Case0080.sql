-- @testpoint: 匿名块使用操作符 |/  平方根

DROP TABLE IF EXISTS test_procedure_insert_080;
create table test_procedure_insert_080 (id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_080 (SELECT |/ 25.0 AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_080;
drop table test_procedure_insert_080;