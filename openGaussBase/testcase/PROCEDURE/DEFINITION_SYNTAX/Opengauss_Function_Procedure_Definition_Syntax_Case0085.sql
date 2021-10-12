-- @testpoint: 匿名块使用操作符 ~ 二进制NOT

DROP TABLE IF EXISTS test_procedure_insert_085;
create table test_procedure_insert_085(id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_085(SELECT ~1 AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_085;
drop table test_procedure_insert_085;