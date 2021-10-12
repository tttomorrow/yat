-- @testpoint: 关键字xmlelement，用作字段名

drop table if exists xmlelement_test cascade;
create table xmlelement_test(id int,xmlelement varchar(20));

create or replace procedure xmlelement_insert
as
begin
 for i in 1..10 loop
    insert into xmlelement_test values(i,'val+'||i);
    end loop;
 end;
/
call xmlelement_insert();

select * from xmlelement_test;
drop table if exists xmlelement_test cascade;
drop procedure xmlelement_insert;