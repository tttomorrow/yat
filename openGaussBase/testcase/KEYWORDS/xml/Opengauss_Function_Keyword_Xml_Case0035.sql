-- @testpoint: 关键字xml，用作表名创建普通表

drop table if exists xml cascade;
create table xml(id int,name varchar(20));

create or replace procedure xml_insert
as
begin
 for i in 1..10 loop
    insert into xml values(i,'att+'||i);
    end loop;
 end;
/
call xml_insert();

select * from xml;
drop table if exists xml cascade;
drop procedure xml_insert;