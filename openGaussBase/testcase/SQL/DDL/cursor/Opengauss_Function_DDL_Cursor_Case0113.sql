--  @testpoint:结合存储过程，显式游标，定义动态游标，提取游标到不匹配的变量类型，合理报错；

--前置条件
drop table if exists cur_test_113;
create table cur_test_113(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_113 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标的使用,提取游标到不匹配的变量类型；
drop procedure if exists cursor_ftest_113;
create or replace procedure cursor_ftest_113()
as
declare
    fet_city int;
    type cursor_type is ref cursor;
    c113 cursor_type;
    sql_str varchar(100);
begin
    sql_str := 'select c_city from cur_test_113 where c_id >= 5;';
    open c113 for sql_str;
    fetch c113 into fet_city;
    raise info 'fetch results:%',fet_city;
    close c113;
end;
/

call cursor_ftest_113();
drop table cur_test_113;
drop procedure cursor_ftest_113;
