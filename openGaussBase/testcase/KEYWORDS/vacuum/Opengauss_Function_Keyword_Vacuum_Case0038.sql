-- @testpoint: 关键字vacuum,用作表名创建普通表

drop table if exists vacuum cascade;
create table vacuum(id int,name varchar(20));

create or replace procedure vacuum_insert
as
begin
 for i in 1..10 loop
    insert into vacuum values(i,'vac+'||i);
    end loop;
 end;
/
call vacuum_insert();

select * from vacuum;
drop table if exists vacuum cascade;
drop procedure vacuum_insert;