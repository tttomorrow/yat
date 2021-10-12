-- @testpoint: 关键字variable，用作字段名


drop table if exists variable_test cascade;
create table variable_test(id int,variable varchar(20));

create or replace procedure variable_insert
as
begin
 for i in 1..10 loop
    insert into variable_test values(i,'vari+'||i);
    end loop;
 end;
/
call variable_insert();

select * from variable_test;

drop table if exists variable_test cascade;
drop procedure variable_insert;
