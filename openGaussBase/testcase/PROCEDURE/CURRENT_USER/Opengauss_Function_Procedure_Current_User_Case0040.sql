-- @testpoint: 存储过程嵌套带有事务管理的函数，调用函数 合理报错

--step1：创建表; expect:成功
drop table if exists test1;
create table test1 (a int);

--step2: 创建带有事物的存储过程; expect: 成功
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

--step3: 调用存储过程; expect: 成功
call transaction_test1();

--step4: 调用函数; expect: 成功
call func_increment_sql(1,2,3);

--step5: 查看表数据; expect: 数据插入成功
select * from test1;

--step6: 清理环境; expect: 清理环境成功
drop table if exists test1;
drop procedure transaction_test1;
drop function func_increment_sql;
