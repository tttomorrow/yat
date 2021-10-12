-- @testpoint: 关键字xmlroot，用作字段类型（合理报错）

drop table if exists xmlroot_test cascade;
create table xmlroot_test(id int,name xmlroot);

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
drop procedure xmlroot_insert;