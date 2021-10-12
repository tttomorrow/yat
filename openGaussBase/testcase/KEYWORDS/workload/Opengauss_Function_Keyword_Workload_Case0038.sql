-- @testpoint: 关键字workload，用作字段类型(合理报错)

drop table if exists workload_test cascade;
create table workload_test(id int,name workload(20));

create or replace procedure workload_insert
as
begin
 for i in 1..10 loop
    insert into workload_test values(i,'work'||i);
    end loop;
 end;
/
call workload_insert();

select * from workload_test;
drop procedure workload_insert;