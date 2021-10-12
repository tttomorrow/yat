-- @testpoint: 匿名块使用操作符 >>二进制右移

DROP TABLE IF EXISTS test_procedure_insert_087;
create table test_procedure_insert_087(id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_087(SELECT 8>>2 AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_087;
drop table test_procedure_insert_087;