-- @testpoint: 关键字value，用作字符串

drop table if exists value_test cascade;
create table value_test(id int,value varchar(20));

create or replace procedure value_insert
as
begin
 for i in 1..10 loop
    insert into value_test values(i,'value');
    end loop;
 end;
/
call value_insert();

select * from value_test;
drop table if exists value_test cascade;
drop procedure value_insert;