-- @testpoint: 关键字validation,用作表名创建普通表

drop table if exists validation cascade;
create table validation(id int,name varchar(20));

create or replace procedure validation_insert
as
begin
 for i in 1..10 loop
    insert into validation values(i,'vali+'||i);
    end loop;
 end;
/
call validation_insert();

select * from validation;
drop table if exists validation cascade;
drop procedure validation_insert;