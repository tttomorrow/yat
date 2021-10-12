-- @testpoint: 匿名块使用数字操作函数  立方根 cbrt(dp)

DROP TABLE IF EXISTS test_procedure_insert_092;
create table test_procedure_insert_092(id double precision,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_092 (SELECT cbrt(27.0), 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_092;
drop table test_procedure_insert_092;


