-- @testpoint: 关键字zone，用作字符串

drop table if exists zone_test cascade;
create table zone_test(id int,name varchar(20));

create or replace procedure zone_insert
as
begin
 for i in 1..20 loop
    insert into zone_test values(i,'zone'||i);
    end loop;
 end;
 /

call zone_insert();

select * from zone_test;
drop table if exists zone_test cascade;
drop procedure zone_insert;
