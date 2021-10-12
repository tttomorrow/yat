-- @testpoint: 关键字xmlattributes，用作字符串

drop table if exists xmlattributes_test cascade;
create table xmlattributes_test(id int,name varchar(20));

create or replace procedure xmlattributes_insert
as
begin
 for i in 1..10 loop
    insert into xmlattributes_test values(i,'xmlattributes'||i);
    end loop;
 end;
/
call xmlattributes_insert();

select * from xmlattributes_test;
drop table if exists xmlattributes_test cascade;
drop procedure xmlattributes_insert;