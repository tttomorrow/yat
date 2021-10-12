-- @testpoint: 关键字within，用作表名创建普通表，部分测试点合理报错

drop table if exists within cascade;
create table within(id int,name varchar(20));

create or replace procedure within_insert
as
begin
 for i in 1..10 loop
    insert into within values(i,'wit+'||i);
    end loop;
 end;
/
call within_insert();

select * from within;
drop table if exists within cascade;
drop procedure within_insert;