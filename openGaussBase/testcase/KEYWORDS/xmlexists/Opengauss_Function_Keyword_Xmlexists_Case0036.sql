-- @testpoint: 关键字xmlexists，用作字符串

drop table if exists xmlexists_test cascade;
create table xmlexists_test(id int,name varchar(20));

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
drop table if exists xmlexists_test cascade;
drop procedure xmlexists_insert;