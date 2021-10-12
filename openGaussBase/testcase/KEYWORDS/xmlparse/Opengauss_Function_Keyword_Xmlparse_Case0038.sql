-- @testpoint: 关键字xmlparse，用作字段类型(合理报错)

drop table if exists xmlparse_test cascade;
create table xmlparse_test(id int,name xmlparse(20));

create or replace procedure xmlparse_insert
as
begin
 for i in 1..10 loop
    insert into xmlparse_test values(i,'xmlparse'||i);
    end loop;
 end;
/
call xmlparse_insert();

select * from xmlparse_test;
drop procedure xmlparse_insert;