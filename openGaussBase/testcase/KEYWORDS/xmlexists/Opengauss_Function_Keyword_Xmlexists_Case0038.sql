-- @testpoint: 关键字xmlexists，用作字段类型(合理报错)

drop table if exists xmlexists_test cascade;
create table xmlexists_test(id int,name xmlexists(20));

create or replace procedure xmlexists_insert
as
begin
 for i in 1..10 loop
    insert into xmlexists_test values(i,'xmlexists'||i);
    end loop;
 end;
/
call xmlexists_insert();

select * from xmlexists_test;
drop procedure xmlexists_insert;