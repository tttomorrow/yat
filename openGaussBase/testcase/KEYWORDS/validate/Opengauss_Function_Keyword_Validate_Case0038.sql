-- @testpoint: 关键字validate,用作字段类型（合理报错）

drop table if exists validate_test cascade;
create table validate_test(id int,name validate(20));

create or replace procedure validate_insert
as
begin
 for i in 1..10 loop
    insert into validate_test values(i,'vali'||i);
    end loop;
 end;
/
call validate_insert();

select * from validate_test;
drop procedure validate_insert;