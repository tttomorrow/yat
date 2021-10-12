-- @testpoint: 关键字variable，用作字符串


drop table if exists variable_test cascade;
create table variable_test(id int,name varchar(20));

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
drop table if exists variable_test cascade;
drop procedure variable_insert;

