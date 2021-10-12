-- @testpoint: 关键字unencrypted，用作表名创建普通表


drop table if exists unencrypted cascade;
create table if not exists unencrypted(id int,name varchar(20));

create or replace procedure unencrypted_insert
as
begin
 for i in 1..10 loop
    insert into unencrypted values(i,'unencry+'||i);
    end loop;
 end;
/
call unencrypted_insert();

select * from unencrypted;

--清理环境
drop table if exists unencrypted cascade;
drop procedure unencrypted_insert;