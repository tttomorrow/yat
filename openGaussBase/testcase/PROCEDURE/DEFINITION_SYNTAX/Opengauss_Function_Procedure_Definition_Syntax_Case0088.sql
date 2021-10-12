-- @testpoint: 匿名块使用数字操作函数 acos(x)

DROP TABLE IF EXISTS test_procedure_insert_088;
create table test_procedure_insert_088(id double precision,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_088 (SELECT acos(-1), 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_088;
drop table test_procedure_insert_088;