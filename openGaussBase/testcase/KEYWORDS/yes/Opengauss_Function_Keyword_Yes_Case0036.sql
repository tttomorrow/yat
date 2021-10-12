-- @testpoint: 关键字yes，用作表名创建普通表

drop table if exists yes cascade;
create table yes(id int,name varchar(20));

create or replace procedure yes_insert
as
begin
 for i in 1..20 loop
    insert into yes values(i,'a'||i);
    end loop;
 end;
/
call yes_insert();

select * from yes;
drop table if exists yes cascade;
drop procedure yes_insert;
