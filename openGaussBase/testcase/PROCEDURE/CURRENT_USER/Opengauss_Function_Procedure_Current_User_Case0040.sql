-- @testpoint: 存储过程嵌套带有事务管理的函数，调用函数 合理报错
drop table if exists test1;
create table test1 (a int);
--创建带有事物的存储过程
create or replace procedure transaction_test1()
as
begin
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
end;
/
--调用存储过程 成功
call transaction_test1();

--调用函数 合理报错
call func_increment_sql(1,2,3);

--查看表数据
select * from test1;

--清理环境
drop table if exists test1;
drop procedure transaction_test1;
drop function func_increment_sql;
