-- @testpoint: 关键字xmlroot，用作表名创建普通表

drop table if exists xmlroot cascade;
create table xmlroot(id int,name varchar(20));

create or replace procedure xmlroot_insert
as
begin
 for i in 1..20 loop
    insert into xmlroot values(i,'a'||i);
    end loop;
 end;
/
call xmlroot_insert();

select * from xmlroot;
drop table if exists xmlroot cascade;
drop procedure xmlroot_insert;