-- @testpoint: 关键字xmlserialize，用作字段名

drop table if exists xmlserialize_test cascade;
create table xmlserialize_test(id int,xmlserialize varchar(20));

create or replace procedure xmlserialize_insert
as
begin
 for i in 1..20 loop
    insert into xmlserialize_test values(i,'a'||i);
    end loop;
 end;
/
call xmlserialize_insert();

select * from xmlserialize_test;
drop table if exists xmlserialize_test cascade;
drop procedure xmlserialize_insert;