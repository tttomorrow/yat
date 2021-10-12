--  @testpoint:结合存储过程，显式游标，定义静态游标，提取游标到匹配的变量类型；

--前置条件
drop table if exists cur_test_106;
create table cur_test_106(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_106 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标的使用,提取游标到匹配的变量类型；
drop procedure if exists cursor_ftest_106;
create or replace procedure cursor_ftest_106()
as
declare
    fet_city varchar(10);
    cursor c106 is select c_city from cur_test_106 where c_id <= 5;
begin
    open c106;
    fetch c106 into fet_city;
    raise info 'fetch results:%',fet_city;
    close c106;
end;
/

call cursor_ftest_106();
drop table cur_test_106;
drop procedure cursor_ftest_106;
