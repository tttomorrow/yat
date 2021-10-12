-- @testpoint: 关键字variable，用作字段类型（合理报错）


drop table if exists variable_test cascade;
create table variable_test(id int,name variable(20));

create or replace procedure variable_insert
as
begin
 for i in 1..10 loop
    insert into variable_test values(i,'variable');
    end loop;
 end;
/
call variable_insert();

select * from variable_test;
drop procedure variable_insert;

