-- @testpoint: 表与自定义函数

drop table if exists tab135;
create table tab135(a jsonb);
insert into tab135 values('1'),('5'),('10');
create or replace function fun_for_return_query() returns setof tab135 as $$
declare
   r tab135%rowtype;
begin
   return query select * from tab135;
end;
$$ language plpgsql;
/
call fun_for_return_query();
drop function if exists fun_for_return_query();
drop table if exists tab135 cascade;