--  @testpoint:结合存储过程，显式游标，定义动态游标，提取游标到匹配的变量类型；

--前置条件
drop table if exists cur_test_112;
create table cur_test_112(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_112 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标的使用,提取游标到匹配的变量类型；
drop procedure if exists cursor_ftest_112;
create or replace procedure cursor_ftest_112()
as
declare
    fet_num int;
    type cursor_type is ref cursor;
    c112 cursor_type;
    sql_str varchar(100);
begin
    sql_str := 'select c_num from cur_test_112 where c_id <= 5;';
    open c112 for sql_str;
    fetch c112 into fet_num;
    raise info 'fetch results:%',fet_num;
    close c112;
end;
/

call cursor_ftest_112();
drop table cur_test_112;
drop procedure cursor_ftest_112;
