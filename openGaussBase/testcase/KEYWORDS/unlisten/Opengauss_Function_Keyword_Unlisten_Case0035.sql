-- @testpoint: 关键字unlisten，用作表名创建普通表


drop table if exists unlisten cascade;
create table if not exists unlisten(id int,name varchar(20));

create or replace procedure unlisten_insert
as
begin
 for i in 1..10 loop
    insert into unlisten values(i,'unlis+'||i);
    end loop;
 end;
/
call unlisten_insert();

select * from unlisten;

--清理环境
drop table if exists unlisten cascade;
drop procedure unlisten_insert;