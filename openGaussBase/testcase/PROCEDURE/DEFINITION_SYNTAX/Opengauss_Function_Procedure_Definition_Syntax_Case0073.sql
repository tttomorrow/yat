-- @testpoint: 匿名块使用操作符 阶乘操作符 ！

DROP TABLE IF EXISTS test_procedure_insert_01;
create table test_procedure_insert_01 (f1 bigint, f2 int);

declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_01 (select 6! , 3)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_01;
drop table if exists test_procedure_insert_01;








