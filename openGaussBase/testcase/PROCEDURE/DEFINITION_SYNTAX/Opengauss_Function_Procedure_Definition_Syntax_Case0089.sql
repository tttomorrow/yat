-- @testpoint: 匿名块使用数字操作函数  反正弦 asin(x)

DROP TABLE IF EXISTS test_procedure_insert_089;
create table test_procedure_insert_089(id double precision,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_089 (SELECT asin(0.5), 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_089;
drop table test_procedure_insert_089;

