-- @testpoint: 匿名块使用操作符 字符串连接操作符 ||

DROP TABLE IF EXISTS test_procedure_insert_074;
create table test_procedure_insert_074 (id int,
name varchar2(20));
begin
 FOR I IN 1 .. 10 LOOP
    insert into test_procedure_insert_074  values (I,'ÀîÃ÷'||i);
 END LOOP;
end;
/

select * from test_procedure_insert_074;
drop table test_procedure_insert_074;


