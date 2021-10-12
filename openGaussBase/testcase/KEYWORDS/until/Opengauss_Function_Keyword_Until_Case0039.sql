-- @testpoint: 关键字until,用作字段类型（合理报错）

drop table if exists until_test cascade;
create table if not exists until_test(id int,name until(20));

create or replace procedure until_insert
as
begin
 for i in 1..10 loop
    insert into until_test values(i,'until'||i);
    end loop;
 end;
/
call until_insert();

select * from until_test;

--清理环境
drop procedure until_insert;