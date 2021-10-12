--  @testpoint:结合存储过程，显式游标，属性%FOUND的使用；

--前置条件
drop table if exists cur_test_116;
create table cur_test_116(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_116 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标属性%FOUND的使用；
drop procedure if exists cursor_ftest_116;
create or replace procedure cursor_ftest_116()
as
declare
    fet_city varchar(10);
    cursor c116 is select c_city from cur_test_116 where c_id <= 5;
begin
    open c116;
    fetch c116 into fet_city;
    raise info 'fetch results:%',fet_city;
    close c116;
    exit when c116%found;
end;
/

call cursor_ftest_116();
drop table cur_test_116;
drop procedure cursor_ftest_116;
