-- @testpoint: 关键字usage，作为字段名


drop table if exists usage_test cascade;
create table usage_test(id int,usage varchar(20));

create or replace procedure usage_insert
as
begin
 for i in 1..10 loop
    insert into usage_test values(i,'usa+'||i);
    end loop;
 end;
/
call usage_insert();

select * from usage_test;
drop table if exists usage_test cascade;
drop procedure usage_insert;