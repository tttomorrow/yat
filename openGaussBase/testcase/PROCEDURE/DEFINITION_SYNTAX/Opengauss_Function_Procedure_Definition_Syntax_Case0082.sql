-- @testpoint: 匿名块使用操作符 &二进制AND

DROP TABLE IF EXISTS test_procedure_insert_082;
create table test_procedure_insert_082(id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_082(SELECT 91&15  AS RESULT, 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_082;
drop table test_procedure_insert_082;
