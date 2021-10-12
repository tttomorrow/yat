--  @testpoint:结合存储过程，隐式游标，结合insert into语句，属性%ISOPEN的使用；

--前置条件
drop table if exists cur_test_138;
create table cur_test_138(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_138 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，结合insert into语句，隐式游标属性%ISOPEN，取值总为False(默认执行完SQL后立马关闭)，不会影响下一步语句执行结果；
drop procedure if exists cursor_ftest_138;
create or replace procedure cursor_ftest_138()
as
begin
    insert into cur_test_138(c_id) values(7);
    if sql%isopen then
        update cur_test_138 set c_add = 'ABCDEFG' where c_id = 7;
    end if;
end;
/

call cursor_ftest_138();
select * from cur_test_138 where c_id = 7;
drop table cur_test_138;
drop procedure cursor_ftest_138;
