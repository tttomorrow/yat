-- @testpoint: 关键字yes，用作字符串

drop table if exists yes_test cascade;
create table yes_test(id int,name varchar(20));

create or replace procedure yes_insert
as
begin
 for i in 1..20 loop
    insert into yes_test values(i,'yes'||i);
    end loop;
 end;
/
call yes_insert();

select * from yes_test;
drop table if exists yes_test cascade;
drop procedure yes_insert;