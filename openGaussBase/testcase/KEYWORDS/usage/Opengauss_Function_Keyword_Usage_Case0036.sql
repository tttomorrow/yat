-- @testpoint: 关键字usage，作为表名创建普通表


drop table if exists usage cascade;
create table usage(id int,name varchar(20));

create or replace procedure usage_insert
as
begin
 for i in 1..10 loop
    insert into usage values(i,'usa+'||i);
    end loop;
 end;
/
call usage_insert();

select * from usage;
drop table if exists usage cascade;
drop procedure usage_insert;