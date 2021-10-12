-- @testpoint: 关键字xmlexists，用作表名创建普通表

drop table if exists xmlexists cascade;
create table xmlexists(id int,name varchar(20));

create or replace procedure xmlexists_insert
as
begin
 for i in 1..10 loop
    insert into xmlexists values(i,'xml+'||i);
    end loop;
 end;
/
call xmlexists_insert();

select * from xmlexists;
drop table if exists xmlexists cascade;
drop procedure xmlexists_insert;