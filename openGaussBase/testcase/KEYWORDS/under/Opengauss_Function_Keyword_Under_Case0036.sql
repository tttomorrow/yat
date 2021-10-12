-- @testpoint: 关键字under,用作字段名

drop table if exists under_test cascade;
create table if not exists under_test(id int,under varchar(20));

create or replace procedure under_insert
as
begin
 for i in 1..10 loop
    insert into under_test values(i,'und+'||i);
    end loop;
 end;
/
call under_insert();

select * from under_test;

--清理环境
drop table if exists under_test cascade;
drop procedure under_insert;