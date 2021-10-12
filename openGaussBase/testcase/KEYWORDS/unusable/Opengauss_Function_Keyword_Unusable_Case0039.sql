-- @testpoint: 关键字unusable,用作字段类型（合理报错）

drop table if exists unusable_test cascade;
create table if not exists unusable_test(id int,unusable unusable(20));

create or replace procedure unusable_insert
as
begin
 for i in 1..10 loop
    insert into unusable_test values(i,'unusable'||i);
    end loop;
 end;
/
call unusable_insert();

select * from unusable_test;

--清理环境
drop procedure unusable_insert;