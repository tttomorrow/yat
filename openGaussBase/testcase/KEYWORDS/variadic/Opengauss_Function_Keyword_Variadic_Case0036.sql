-- @testpoint: 关键字variadic（保留），用作表名创建普通表（合理报错）


drop table if exists variadic cascade;
create table variadic(id int,name varchar(20));

create or replace procedure variadic_insert
as
begin
 for i in 1..10 loop
    insert into variadic values(i,'vari+'||i);
    end loop;
 end;
/
call variadic_insert();

select * from variadic;


