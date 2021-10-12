-- @testpoint: 关键字xmlconcat，用作字段类型(合理报错)

drop table if exists xmlconcat_test cascade;
create table xmlconcat_test(id int,name xmlconcat(20));

create or replace procedure xmlconcat_insert
as
begin
 for i in 1..10 loop
    insert into xmlconcat_test values(i,'xmlconcat'||i);
    end loop;
 end;
/
call xmlconcat_insert();

select * from xmlconcat_test;
drop procedure xmlconcat_insert;