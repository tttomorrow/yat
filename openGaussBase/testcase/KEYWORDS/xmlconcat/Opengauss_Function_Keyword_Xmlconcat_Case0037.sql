-- @testpoint: 关键字xmlconcat，用作字段名

drop table if exists xmlconcat_test cascade;
create table xmlconcat_test(id int,xmlconcat varchar(20));

create or replace procedure xmlconcat_insert
as
begin
 for i in 1..10 loop
    insert into xmlconcat_test values(i,'val+'||i);
    end loop;
 end;
/
call xmlconcat_insert();

select * from xmlconcat_test;
drop table if exists xmlconcat_test cascade;
drop procedure xmlconcat_insert;