-- @testpoint: 关键字with，用作字段名（合理报错）

drop table if exists with_test cascade;
create table with_test(id int,with varchar(20));

create or replace procedure with_insert
as
begin
 for i in 1..10 loop
    insert into with_test values(i,'with'||i);
    end loop;
 end;
/
call with_insert();

select * from with_test;
drop procedure with_insert;

