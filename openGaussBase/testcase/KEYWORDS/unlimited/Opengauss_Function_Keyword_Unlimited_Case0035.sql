-- @testpoint: 关键字unlimited,用作表名创建普通表


drop table if exists unlimited cascade;
create table if not exists unlimited(id int,name varchar(20));

create or replace procedure unlimited_insert
as
begin
 for i in 1..10 loop
    insert into unlimited values(i,'unlimi+'||i);
    end loop;
 end;
/
call unlimited_insert();

select * from unlimited;

--清理环境
drop table if exists unlimited cascade;
drop procedure unlimited_insert;