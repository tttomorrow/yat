-- @testpoint: 关键字unlisten，用作字符串


drop table if exists unlisten_test cascade;
create table if not exists unlisten_test(id int,unlisten varchar);

create or replace procedure unlisten_insert
as
begin
 for i in 1..10 loop
    insert into unlisten_test values(i,'unlisten');
    end loop;
 end;
/
call unlisten_insert();

select * from unlisten_test;

--清理环境
drop table if exists unlisten_test cascade;
drop procedure unlisten_insert;