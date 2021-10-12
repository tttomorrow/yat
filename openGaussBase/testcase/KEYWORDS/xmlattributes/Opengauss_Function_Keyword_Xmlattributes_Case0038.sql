-- @testpoint: 关键字xmlattributes，用作字段类型(合理报错)

drop table if exists xmlattributes_test cascade;
create table xmlattributes_test(id int,name xmlattributes(20));

create or replace procedure xmlattributes_insert
as
begin
 for i in 1..10 loop
    insert into xmlattributes_test values(i,'attributes'||i);
    end loop;
 end;
/
call xmlattributes_insert();

select * from xmlattributes_test;
drop procedure xmlattributes_insert;