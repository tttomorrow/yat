-- @testpoint: 关键字xmlattributes，用作表名创建普通表

drop table if exists xmlattributes cascade;
create table xmlattributes(id int,name varchar(20));

create or replace procedure xmlattributes_insert
as
begin
 for i in 1..10 loop
    insert into xmlattributes values(i,'attributes+'||i);
    end loop;
 end;
/
call xmlattributes_insert();

select * from xmlattributes;
drop table if exists xmlattributes cascade;
drop procedure xmlattributes_insert;