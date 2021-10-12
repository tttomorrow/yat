-- @testpoint: 关键字until,用作表名创建普通表

drop table if exists until cascade;
create table if not exists until(id int,name varchar(20));

create or replace procedure until_insert
as
begin
 for i in 1..10 loop
    insert into until values(i,'unt+'||i);
    end loop;
 end;
/
call until_insert();

select * from until;

--清理环境
drop table if exists until cascade;
drop procedure until_insert;