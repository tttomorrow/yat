-- @testpoint: 关键字varying,用作数据类型，部分测试点合理报错

drop table if exists vary_test cascade;
create table vary_test(id int,name character varying(20));

create or replace procedure varying_insert
as
begin
 for i in 1..10 loop
    insert into vary_test values(i,'vary+'||i);
    end loop;
 end;
/
call varying_insert();

select * from vary_test;
drop table if exists vary_test cascade;
drop procedure varying_insert;