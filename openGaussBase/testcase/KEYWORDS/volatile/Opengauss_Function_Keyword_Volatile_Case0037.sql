-- @testpoint: 关键字volatile,用作字符串

drop table if exists volatile_test cascade;
create table volatile_test(id int,name varchar(20));

create or replace procedure volatile_insert
as
begin
 for i in 1..10 loop
    insert into volatile_test values(i,'volatile'||i);
    end loop;
 end;
/
call volatile_insert();

select * from volatile_test;
drop table if exists volatile_test cascade;
drop procedure volatile_insert;