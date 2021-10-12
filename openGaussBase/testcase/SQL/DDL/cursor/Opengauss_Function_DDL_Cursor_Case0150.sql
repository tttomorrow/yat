--  @testpoint:结合存储过程，隐式游标，结合create语句，属性%ISOPEN的使用；

--前置条件
drop table if exists cur_test_150;
create table cur_test_150(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_150 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA');

--创建存储过程，结合create语句，隐式游标属性%ISOPEN,取值总为False(默认执行完SQL后立马关闭)，不会影响下一步语句执行结果；
drop procedure if exists cursor_ftest_150;
create or replace procedure cursor_ftest_150()
as
begin
    create table test_150(id int);
    if sql%isopen then
        delete from cur_test_150 where c_id <= 3;
    end if;
end;
/

call cursor_ftest_150();

--属性未生效，不影响下一步SQL执行结果
select * from cur_test_150;
drop table cur_test_150;
drop table test_150;
drop procedure cursor_ftest_150;
