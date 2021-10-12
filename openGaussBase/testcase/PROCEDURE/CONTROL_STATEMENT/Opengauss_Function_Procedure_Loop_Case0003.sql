-- @testpoint: while_loop语句

create table integertable(c1 integer) ;
create or replace procedure proc_while_loop(maxval in integer)
as
    declare
    i int :=1;
    begin
        while i < maxval loop
            insert into integertable values(i);
            i:=i+1;
        end loop;
    end;
/

--调用函数
call proc_while_loop(10);

--删除存储过程和表
drop procedure proc_while_loop;
drop table integertable;
