-- @testpoint: 关键字usage，作为字段类型，合理报错


drop table if exists usage_test cascade;
create table usage_test(id int,name usage);

create or replace procedure usage_insert
as
begin
 for i in 1..10 loop
    insert into usage_test values(i,'usage'||i);
    end loop;
 end;
/
call usage_insert();
drop procedure usage_insert;