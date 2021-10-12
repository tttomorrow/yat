-- @testpoint: 匿名块使用数字操作函数  sin(x)

DROP TABLE IF EXISTS test_procedure_insert_118;
create table test_procedure_insert_118(id double precision,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_118 (SELECT sin(1.57079),44)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_118;
drop table test_procedure_insert_118;
