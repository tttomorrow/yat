-- @testpoint: 关键字xmlparse，用作表名创建普通表

drop table if exists xmlparse cascade;
create table xmlparse(id int,name varchar(20));

create or replace procedure xmlparse_insert
as
begin
 for i in 1..10 loop
    insert into xmlparse values(i,'a+'||i);
    end loop;
 end;
/
call xmlparse_insert();

select * from xmlparse;
drop table if exists xmlparse cascade;
drop procedure xmlparse_insert;