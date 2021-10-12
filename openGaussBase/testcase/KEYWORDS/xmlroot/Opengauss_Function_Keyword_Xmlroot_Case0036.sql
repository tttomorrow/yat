-- @testpoint: 关键字xmlroot，用作字段名

drop table if exists xmlroot_test cascade;
create table xmlroot_test(id int,xmlroot varchar(20));

create or replace procedure xmlroot_insert
as
begin
 for i in 1..20 loop
    insert into xmlroot_test values(i,'a'||i);
    end loop;
 end;
/
call xmlroot_insert();

select * from xmlroot_test;
drop table if exists xmlroot_test cascade;
drop procedure xmlroot_insert;