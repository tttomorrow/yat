-- @testpoint: 匿名块使用数字操作函数  y/x的反正切 atan2(y, x)

DROP TABLE IF EXISTS test_procedure_insert_091;
create table test_procedure_insert_091(id double precision,
name varchar2(20));
declare
sqlstr varchar(1024);
begin
sqlstr := 'insert into test_procedure_insert_091 (SELECT atan2(2, 1), 5)';
execute immediate sqlstr;
end;
/

select * from test_procedure_insert_091;
drop table test_procedure_insert_091;