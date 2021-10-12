-- @testpoint: 关键字xmlpi，用作字段名

drop table if exists xmlpi_test cascade;
create table xmlpi_test(id int,xmlpi varchar(20));

create or replace procedure xmlpi_insert
as
begin
 for i in 1..20 loop
    insert into xmlpi_test values(i,'a'||i);
    end loop;
 end;
/
call xmlpi_insert();

select * from xmlpi_test;
drop table if exists xmlpi_test cascade;
drop procedure xmlpi_insert;