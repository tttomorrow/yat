-- @testpoint: 关键字value，用作表名创建普通表

drop table if exists value cascade;
create table value(id int,name varchar(20));

create or replace procedure value_insert
as
begin
 for i in 1..10 loop
    insert into value values(i,'val+'||i);
    end loop;
 end;
/
call value_insert();

select * from value;
drop table if exists value cascade;
drop procedure value_insert;