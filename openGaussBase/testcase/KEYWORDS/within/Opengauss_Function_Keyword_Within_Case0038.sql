-- @testpoint: 关键字within，用作字段类型(合理报错)

drop table if exists within_test cascade;
create table within_test(id int,name within(20));

create or replace procedure within_insert
as
begin
 for i in 1..10 loop
    insert into within_test values(i,'work'||i);
    end loop;
 end;
/
call within_insert();

select * from within_test;
drop procedure within_insert;