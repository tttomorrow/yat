-- @testpoint: 关键字under,用作表名创建普通表

drop table if exists under cascade;
create table if not exists under(id int,name varchar(20));

create or replace procedure under_insert
as
begin
 for i in 1..10 loop
    insert into under values(i,'und+'||i);
    end loop;
 end;
/
call under_insert();

select * from under;

--清理环境
drop table if exists under cascade;
drop procedure under_insert;