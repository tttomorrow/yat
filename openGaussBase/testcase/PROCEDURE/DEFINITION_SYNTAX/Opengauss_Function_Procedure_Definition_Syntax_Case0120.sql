-- @testpoint: 匿名块使用数字操作函数  pi()

DROP TABLE IF EXISTS test_procedure_insert_120;
create table test_procedure_insert_120(id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_120 (SELECT pi(),44)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_120;
drop table test_procedure_insert_120;