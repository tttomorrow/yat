-- @testpoint: 关键字xmlexists，用作字段名

drop table if exists xmlexists_test cascade;
create table xmlexists_test(id int,xmlexists varchar(20));

create or replace procedure xmlexists_insert
as
begin
 for i in 1..10 loop
    insert into xmlexists_test values(i,'val'||i);
    end loop;
 end;
/
call xmlexists_insert();

select * from xmlexists_test;
drop table if exists xmlexists_test cascade;
drop procedure xmlexists_insert;