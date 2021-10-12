-- @testpoint: 关键字validate,用作字符串

drop table if exists validate_test cascade;
create table validate_test(id int,validation varchar(20));

create or replace procedure validate_insert
as
begin
 for i in 1..10 loop
    insert into validate_test values(i,'validate');
    end loop;
 end;
/
call validate_insert();

select * from validate_test;
drop table if exists validate_test cascade;
drop procedure validate_insert;