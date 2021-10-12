-- @testpoint: 关键字validation,用作字符串

drop table if exists validation_test cascade;
create table validation_test(id int,validation varchar(20));

create or replace procedure validation_insert
as
begin
 for i in 1..10 loop
    insert into validation_test values(i,'validation');
    end loop;
 end;
/
call validation_insert();

select * from validation_test;
drop table if exists validation_test cascade;
drop procedure validation_insert;