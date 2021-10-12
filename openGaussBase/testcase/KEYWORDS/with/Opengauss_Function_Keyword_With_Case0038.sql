-- @testpoint: 关键字with，用作表名创建普通表(合理报错)

drop table if exists with cascade;
create table with(id int,name varchar(20));

create or replace procedure with_insert
as
begin
 for i in 1..10 loop
    insert into with values(i,'wit+'||i);
    end loop;
 end;
/
call with_insert();

select * from with;

