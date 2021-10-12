-- @testpoint: 关键字xmlconcat，用作表名创建普通表

drop table if exists xmlconcat cascade;
create table xmlconcat(id int,name varchar(20));

create or replace procedure xmlconcat_insert
as
begin
 for i in 1..10 loop
    insert into xmlconcat values(i,'concat+'||i);
    end loop;
 end;
/
call xmlconcat_insert();

select * from xmlconcat;
drop table if exists xmlconcat cascade;
drop procedure xmlconcat_insert;