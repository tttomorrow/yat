-- @testpoint: 关键字volatile,用作表名创建普通表

drop table if exists volatile cascade;
create table volatile(id int,name varchar(20));

create or replace procedure volatile_insert
as
begin
 for i in 1..10 loop
    insert into volatile values(i,'vola+'||i);
    end loop;
 end;
/
call volatile_insert();

select * from volatile;
drop table if exists volatile cascade;
drop procedure volatile_insert;