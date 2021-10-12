-- @testpoint: 存储过程中创建带有游标的事务管理 先commit 后rollback

--创建测试表1
drop table if exists test1;
create table test1 (a int);

--创建测试表2
drop table if exists test2;
create table test2(x int);
insert into test2 (x) values (1);
insert into test2 (x) values (2);
insert into test2 (x) values (3);

--创建带有游标的事务管理
create or replace procedure transaction_test2()
as
declare
    r record;
begin
    for r in select * from test2 order by x loop
        insert into test1 (a) values (r.x);
        update test2 set x=4 where x=2;
        if r.x/2 =2 then
            commit;
        else
            rollback;
         end if;
    end loop;
end;
/
--调用存储过程
call transaction_test2();

--查看表test1数据
select * from test1;

--清理环境
drop procedure transaction_test2;
drop table if exists test1;
drop table if exists test2;