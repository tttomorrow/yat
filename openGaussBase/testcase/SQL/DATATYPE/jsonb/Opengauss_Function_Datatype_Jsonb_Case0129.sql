-- @testpoint: 结合存储过程使用jsonb数据类型

drop procedure if exists proc129;
drop table if exists tab129;
create table tab129(id jsonb);
select * from tab129;
create or replace procedure proc129()
as
begin
    for id in 1..10 loop
        insert into tab129 values('"aaa"');
    end loop;
end;
/
call proc129();

select * from tab129;

drop procedure if exists proc129;
drop table if exists tab129;