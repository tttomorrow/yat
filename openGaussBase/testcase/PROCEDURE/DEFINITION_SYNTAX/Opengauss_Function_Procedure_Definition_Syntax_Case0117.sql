-- @testpoint: 匿名块使用数字操作函数  radians(dp)

DROP TABLE IF EXISTS test_procedure_insert_117;
create table test_procedure_insert_117(id double precision,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_117 (SELECT radians(45.0),44)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_117;
drop table test_procedure_insert_117;