-- @testpoint: 关键字variable，用作表名创建普通表


drop table if exists variable cascade;
create table variable(id int,name varchar(20));

create or replace procedure variable_insert
as
begin
 for i in 1..10 loop
    insert into variable values(i,'vari+'||i);
    end loop;
 end;
/
call variable_insert();

select * from variable;
drop table if exists variable cascade;
drop procedure variable_insert;