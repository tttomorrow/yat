-- @testpoint: 存储过程中进行事务管理 只使用commit

create table test1 (a int);
--创建带有事物的存储过程
create or replace procedure transaction_test1()
as
begin
    for i in 0..9 loop
        insert into test1 (a) values (i);
        if i % 2 = 0 then
            commit;
        end if;
    end loop;
end;
/
--调用存储过程
call transaction_test1();

--查看表数据
select * from test1;

--清理环境
drop table if exists test1;
drop procedure transaction_test1;