--  @testpoint:结合存储过程，隐式游标，结合delete语句，属性%NOTFOUND的使用；

--前置条件
drop table if exists cur_test_130;
create table cur_test_130(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_130 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，结合delete语句，隐式游标属性%NOTFOUND为True,影响下一步语句的执行结果；
drop procedure if exists cursor_ftest_130;
create or replace procedure cursor_ftest_130()
as
declare
    fet_city varchar(10):= 'Xian';
begin
    delete from cur_test_130 where c_city = fet_city;
    if sql%notfound then
        delete from cur_test_130 where c_id >= 4;
    end if;
end;
/

call cursor_ftest_130();
select * from cur_test_130;
drop table cur_test_130;
drop procedure cursor_ftest_130;
