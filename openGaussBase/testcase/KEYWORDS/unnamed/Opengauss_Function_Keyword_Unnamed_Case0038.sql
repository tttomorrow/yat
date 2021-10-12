-- @testpoint: 关键字unnamed，用作字段类型（合理报错）


drop table if exists unnamed_test cascade;
create table if not exists unnamed_test(id int,unnamed unnamed(20));

create or replace procedure unnamed_insert
as
begin
 for i in 1..10 loop
    insert into unnamed_test values(i,'unnamed'||i);
    end loop;
 end;
/
call unnamed_insert();

select * from unnamed_test;

--清理环境
drop table if exists unnamed_test cascade;
drop procedure unnamed_insert;