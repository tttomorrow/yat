-- @testpoint: 关键字unusable,用作字符串

drop table if exists unusable_test cascade;
create table if not exists unusable_test(id int,unusable varchar(20));

create or replace procedure unusable_insert
as
begin
 for i in 1..10 loop
    insert into unusable_test values(i,'unusable');
    end loop;
 end;
/
call unusable_insert();

select * from unusable_test;

--清理环境
drop table if exists unusable_test cascade;
drop procedure unusable_insert;