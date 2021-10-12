-- @testpoint: 匿名块使用数字操作函数  round(x)

DROP TABLE IF EXISTS test_procedure_insert_122;
create table test_procedure_insert_122(id double precision,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_122 (SELECT round(42.4),44)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_122;
drop table test_procedure_insert_122;
