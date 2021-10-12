-- @testpoint: 关键字until,用作字段名

drop table if exists until_test cascade;
create table if not exists until_test(id int,until varchar(20));

create or replace procedure until_insert
as
begin
 for i in 1..10 loop
    insert into until_test values(i,'unt+'||i);
    end loop;
 end;
/
call until_insert();

select * from until_test;

--清理环境
drop table if exists until_test cascade;
drop procedure until_insert;