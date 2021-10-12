-- @testpoint: 关键字xmlforest，用作表名创建普通表

drop table if exists xmlforest cascade;
create table xmlforest(id int,name varchar(20));

create or replace procedure xmlforest_insert
as
begin
 for i in 1..10 loop
    insert into xmlforest values(i,'a'||i);
    end loop;
 end;
/
call xmlforest_insert();

select * from xmlforest;
drop table if exists xmlforest cascade;
drop procedure xmlforest_insert;