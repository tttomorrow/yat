-- @testpoint: 关键字xmlforest，用作字符串

drop table if exists xmlforest_test cascade;
create table xmlforest_test(id int,name varchar(20));

create or replace procedure xmlforest_insert
as
begin
 for i in 1..10 loop
    insert into xmlforest_test values(i,'xmlforest'||i);
    end loop;
 end;
/
call xmlforest_insert();

select * from xmlforest_test;
drop table if exists xmlforest_test cascade;
drop procedure xmlforest_insert;