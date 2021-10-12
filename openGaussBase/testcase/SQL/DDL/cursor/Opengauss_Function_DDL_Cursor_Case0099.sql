--  @testpoint:结合存储过程，定义不同名游标，打开静态游标；

--前置条件
drop table if exists cur_test_99;
create table cur_test_99(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_99 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，定义不同名静态游标
drop procedure if exists cursor_ftest_99;
create or replace procedure cursor_ftest_99()
as
declare
    cursor c99_1 is select c_name from cur_test_99 where c_id <= 5;
    cursor c99_2 for select c_city from cur_test_99 where c_num <= 100;
begin
    open c99_1;
    close c99_1;
    open c99_2;
    close c99_2;
end;
/

call cursor_ftest_99();
drop table cur_test_99;
drop procedure cursor_ftest_99;

