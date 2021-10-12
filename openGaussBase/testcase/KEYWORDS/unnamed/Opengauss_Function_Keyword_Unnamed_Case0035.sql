-- @testpoint: 关键字unnamed，用作表名创建普通表


drop table if exists unnamed cascade;
create table if not exists unnamed(id int,name varchar(20));

create or replace procedure unnamed_insert
as
begin
 for i in 1..10 loop
    insert into unnamed values(i,'unname+'||i);
    end loop;
 end;
/
call unnamed_insert();

select * from unnamed;

--清理环境
drop table if exists unnamed cascade;
drop procedure unnamed_insert;