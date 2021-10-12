-- @testpoint: 关键字zone，用作表名创建普通表

drop table if exists zone cascade;
create table zone(id int,name varchar(20));

create or replace procedure zone_insert
as
begin
 for i in 1..20 loop
    insert into zone values(i,'a'||i);
    end loop;
 end;
/
call zone_insert();

select * from zone;
drop table if exists zone cascade;
drop procedure zone_insert;
