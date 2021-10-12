-- @testpoint: 关键字varying,用作表名创建普通表，部分测试点合理报错

drop table if exists varying cascade;
create table varying(id int,name varchar(20));

create or replace procedure varying_insert
as
begin
 for i in 1..10 loop
    insert into varying values(i,'vary+'||i);
    end loop;
 end;
/
call varying_insert();

select * from varying;
drop table if exists varying cascade;
drop procedure varying_insert;