-- @testpoint: 对表进行vacuum（进行大量更新/删除时）


drop table if exists vacuum_test_03;
create table vacuum_test_03(id_src int,name_src varchar(10));

create or replace procedure vacuum_insert
as
begin
 for i in 1..10 loop
    insert into vacuum_test_03 values(i,'val+'||i);
    end loop;
 end;
/
call vacuum_insert();

create or replace procedure vacuum_delete_01
as
begin
 for i in 1..10 loop
    delete from vacuum_test_03;
    end loop;
 end;
/
call vacuum_delete_01();


vacuum full vacuum_test_03;
drop table if exists vacuum_test_03;
drop procedure vacuum_insert;
drop procedure vacuum_delete_01;