-- @testpoint: 关键字xml，用作字符串

drop table if exists xml_test cascade;
create table xml_test(id int,name varchar(20));

create or replace procedure xml_insert
as
begin
 for i in 1..10 loop
    insert into xml_test values(i,'xml'||i);
    end loop;
 end;
/
call xml_insert();

select * from xml_test;
drop table if exists xml_test cascade;
drop procedure xml_insert;