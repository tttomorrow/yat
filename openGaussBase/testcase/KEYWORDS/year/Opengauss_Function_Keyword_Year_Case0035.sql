-- @testpoint: 关键字year，用作表名创建普通表

drop table if exists year cascade;
create table year(id int,name varchar(20));

create or replace procedure year_insert
as
begin
 for i in 1..20 loop
    insert into year values(i,'a'||i);
    end loop;
 end;
/
call year_insert();

select * from year;
drop table if exists year cascade;
drop procedure year_insert;


