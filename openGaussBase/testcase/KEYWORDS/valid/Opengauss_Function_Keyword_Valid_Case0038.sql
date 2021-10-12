-- @testpoint: 关键字valid,用作字段名

drop table if exists valid_test cascade;
create table valid_test(id int,valid varchar(20));

create or replace procedure valid_insert
as
begin
 for i in 1..10 loop
    insert into valid_test values(i,'val+'||i);
    end loop;
 end;
/
call valid_insert();

select * from valid_test;
drop table if exists valid_test cascade;
drop procedure valid_insert;