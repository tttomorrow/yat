--  @testpoint:结合存储过程，显式游标，定义动态游标，提取多个游标到同一变量；

--前置条件
drop table if exists cur_test_115;
create table cur_test_115(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_115 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标的使用,提取多个游标到同一变量；
drop procedure if exists cursor_ftest_115;
create or replace procedure cursor_ftest_115()
as
declare
    fet_city varchar(10);
    type cursor_type is ref cursor;
    c115_1 cursor_type;
    c115_2 cursor_type;
    c115_3 cursor_type;
    sql_str varchar(100);
begin
    sql_str := 'select c_city from cur_test_115 where c_id >= 5;';
    open c115_1 for sql_str;
    open c115_2 for sql_str;
    open c115_3 for sql_str;
    fetch c115_1 into fet_city;
    raise info 'fetch results1:%',fet_city;
    fetch c115_2 into fet_city;
    raise info 'fetch results2:%',fet_city;
    fetch c115_3 into fet_city;
    raise info 'fetch results3:%',fet_city;
    close c115_1;
    close c115_2;
    close c115_3;
end;
/

call cursor_ftest_115();
drop table cur_test_115;
drop procedure cursor_ftest_115;
