--  @testpoint:结合存储过程，显式游标，定义动态游标，提取同名游标；

--前置条件
drop table if exists cur_test_110;
create table cur_test_110(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_110 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标的使用,提取同名游标；
drop procedure if exists cursor_ftest_110;
create or replace procedure cursor_ftest_110()
as
declare
    fet_add varchar(20);
    type cursor_type is ref cursor;
    c110 cursor_type;
    sql_str varchar(100);
begin
    sql_str := 'select c_add from cur_test_110 where c_id <= 5;';
    open c110 for sql_str;
    fetch c110 into fet_add;
    raise info 'fetch results:%',fet_add;
    close c110;
end;
/

call cursor_ftest_110();
drop table cur_test_110;
drop procedure cursor_ftest_110;
