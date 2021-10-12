-- @testpoint: 匿名块使用操作符 绝对值操作符

DROP TABLE IF EXISTS test_procedure_insert_075;
create table test_procedure_insert_075 (id int,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_075 (SELECT abs(-17.4), 3)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_075;
drop table test_procedure_insert_075;

