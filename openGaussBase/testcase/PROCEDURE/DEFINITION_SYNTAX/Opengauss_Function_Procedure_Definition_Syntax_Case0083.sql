-- @testpoint: 匿名块使用操作符 |二进制or


DROP TABLE IF EXISTS test_procedure_insert_083;
create table test_procedure_insert_083(id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_083(SELECT 32|3  AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_083;
drop table test_procedure_insert_083;