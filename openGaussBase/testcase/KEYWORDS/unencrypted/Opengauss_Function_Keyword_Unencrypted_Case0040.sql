-- @testpoint: 关键字unencrypted，用作字段类型（合理报错）


drop table if exists unencrypted_test cascade;
create table if not exists unencrypted_test(id int,unencrypted unencrypted(20));

create or replace procedure unencrypted_insert
as
begin
 for i in 1..10 loop
    insert into unencrypted_test values(i,'unencry'||i);
    end loop;
 end;
/
call unencrypted_insert();

select * from unencrypted_test;

--清理环境
drop procedure unencrypted_insert;