-- @testpoint: 关键字within，用作字段名

drop table if exists within_test cascade;
create table within_test(id int,within varchar(20));

create or replace procedure within_insert
as
begin
 for i in 1..10 loop
    insert into within_test values(i,'val+'||i);
    end loop;
 end;
/
call within_insert();

select * from within_test;
drop table if exists within_test cascade;
drop procedure within_insert;