-- @testpoint: 关键字xmlserialize，用作表名创建普通表

drop table if exists xmlserialize cascade;
create table xmlserialize(id int,name varchar(20));

create or replace procedure xmlserialize_insert
as
begin
 for i in 1..20 loop
    insert into xmlserialize values(i,'a'||i);
    end loop;
 end;
/
call xmlserialize_insert();

select * from xmlserialize;
drop table if exists xmlserialize cascade;
drop procedure xmlserialize_insert;