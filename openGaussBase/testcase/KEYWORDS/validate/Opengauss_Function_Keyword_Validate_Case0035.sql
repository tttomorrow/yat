-- @testpoint: 关键字validate,用作表名创建普通表

drop table if exists validate cascade;
create table validate(id int,name varchar(20));

create or replace procedure validate_insert
as
begin
 for i in 1..10 loop
    insert into validate values(i,'vali+'||i);
    end loop;
 end;
/
call validate_insert();

select * from validate;
drop table if exists validate cascade;
drop procedure validate_insert;
