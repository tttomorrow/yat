-- @testpoint: 匿名块使用操作符 模（求余）

DROP TABLE IF EXISTS test_procedure_insert_078;
create table test_procedure_insert_078 (id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_078 (SELECT 5%4 AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_078;
drop table test_procedure_insert_078;