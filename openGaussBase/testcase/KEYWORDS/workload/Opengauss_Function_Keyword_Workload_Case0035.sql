-- @testpoint: 关键字workload，用作表名创建普通表

drop table if exists workload cascade;
create table workload(id int,name varchar(20));

create or replace procedure workload_insert
as
begin
 for i in 1..10 loop
    insert into workload values(i,'work+'||i);
    end loop;
 end;
/
call workload_insert();

select * from workload;
drop table if exists workload cascade;
drop procedure workload_insert;