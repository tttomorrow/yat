-- @testpoint: 关键字vacuum,用作字段名，部分测试点合理报错

drop table if exists vacuum_test cascade;
create table vacuum_test(id int,vacuum varchar(20));

create or replace procedure vacuum_insert
as
begin
 for i in 1..10 loop
    insert into vacuum_test values(i,'vac+'||i);
    end loop;
 end;
/
call vacuum_insert();

select * from vacuum_test;
drop table if exists vacuum_test cascade;
drop procedure vacuum_insert;