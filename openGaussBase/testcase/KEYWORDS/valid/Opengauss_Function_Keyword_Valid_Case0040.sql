-- @testpoint: 关键字valid,用作字段类型（合理报错）

drop table if exists valid_test cascade;
create table valid_test(id int,valid valid(20));

create or replace procedure valid_insert
as
begin
 for i in 1..10 loop
    insert into valid_test values(i,'valid');
    end loop;
 end;
/
call valid_insert();

select * from valid_test;
drop procedure valid_insert;