-- @testpoint: 关键字xmlelement，用作字段类型(合理报错)

drop table if exists xmlelement_test cascade;
create table xmlelement_test(id int,name xmlelement(20));

create or replace procedure xmlelement_insert
as
begin
 for i in 1..10 loop
    insert into xmlelement_test values(i,'xmlelement'||i);
    end loop;
 end;
/
call xmlelement_insert();

select * from xmlelement_test;
drop procedure xmlelement_insert;