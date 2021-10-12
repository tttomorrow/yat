-- @testpoint: 关键字xmlelement，用作表名创建普通表

drop table if exists xmlelement cascade;
create table xmlelement(id int,name varchar(20));

create or replace procedure xmlelement_insert
as
begin
 for i in 1..10 loop
    insert into xmlelement values(i,'element+'||i);
    end loop;
 end;
/
call xmlelement_insert();

select * from xmlelement;
drop table if exists xmlelement cascade;
drop procedure xmlelement_insert;