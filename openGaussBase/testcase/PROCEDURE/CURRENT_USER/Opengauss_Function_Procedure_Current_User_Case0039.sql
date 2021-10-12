-- @testpoint: 函数中进行事务管理 合理报错

create table test1 (a int);
--创建带有事务管理的函数
create or replace function func_increment_sql(i int, out result_1 bigint, out result_2 bigint)
returns setof record
as $$
begin
for i in 0..9 loop
        insert into test1 (a) values (i);
        if i % 2 = 0 then
            commit;
        else
            rollback;
        end if;
    end loop;
return next;
end;
$$language plpgsql;

--调用函数
call func_increment_sql(1,2,3);

--查看表数据
select * from test1;

--清理环境
drop table if exists test1;
drop function func_increment_sql;