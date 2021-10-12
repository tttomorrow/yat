-- @testpoint: 关键字xmlpi，用作表名创建普通表

drop table if exists xmlpi cascade;
create table xmlpi(id int,name varchar(20));

create or replace procedure xmlpi_insert
as
begin
 for i in 1..20 loop
    insert into xmlpi values(i,'a'||i);
    end loop;
 end;
/
call xmlpi_insert();

select * from xmlpi;
drop table if exists xmlpi cascade;
drop procedure xmlpi_insert;