-- @testpoint: 关键字variadic（保留），用作字符串，部分测试点合理报错


drop table if exists variadic_test cascade;
create table variadic_test(id int,name varchar(20));

create or replace procedure variadic_insert
as
begin
 for i in 1..10 loop
    insert into variadic_test values(i,'variadic');
    end loop;
 end;
/
call variadic_insert();

select * from variadic_test;
drop table if exists variadic_test cascade;
drop procedure variadic_insert;

