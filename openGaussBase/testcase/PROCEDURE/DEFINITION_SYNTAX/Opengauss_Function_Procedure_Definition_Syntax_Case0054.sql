-- @testpoint: 将一个表的数据带括号插入另一个表中

DROP TABLE IF EXISTS test_procedure_insert_01;
create table test_procedure_insert_01 (f1 int, f2 int);
insert into test_procedure_insert_01 values(1,2);
select * from test_procedure_insert_01;
DROP TABLE IF EXISTS test_procedure_insert_02;
create table test_procedure_insert_02 (f1 int, f2 int);
insert into test_procedure_insert_02 (select f1,f2 from test_procedure_insert_01);
select * from test_procedure_insert_02;
DROP TABLE test_procedure_insert_01;
DROP TABLE test_procedure_insert_02;