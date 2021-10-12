-- @testpoint: 关键字valid,用作表名创建普通表

drop table if exists valid cascade;
create table valid(id int,name varchar(20));

create or replace procedure valid_insert
as
begin
 for i in 1..10 loop
    insert into valid values(i,'val+'||i);
    end loop;
 end;
/
call valid_insert();

select * from valid;
drop table if exists valid cascade;
drop procedure valid_insert;