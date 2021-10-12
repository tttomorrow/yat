-- @testpoint: 关键字unusable,用作表名创建普通表

drop table if exists unusable cascade;
create table if not exists unusable(id int,name varchar(20));

create or replace procedure unusable_insert
as
begin
 for i in 1..10 loop
    insert into unusable values(i,'unusa+'||i);
    end loop;
 end;
/
call unusable_insert();

select * from unusable;

--清理环境
drop table if exists unusable cascade;
drop procedure unusable_insert;