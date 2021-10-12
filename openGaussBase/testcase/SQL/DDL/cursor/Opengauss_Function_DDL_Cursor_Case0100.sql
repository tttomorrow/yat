--  @testpoint:结合存储过程，定义同名游标，打开动态游标,合理报错；

--前置条件
drop table if exists cur_test_100;
create table cur_test_100(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_100 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，定义同名动态游标
drop procedure if exists cursor_ftest_100;
create or replace procedure cursor_ftest_100()
as
declare
    type cursor_type is ref cursor;
    c100 cursor_type;
    c100 cursor_type;
    sql_str1 varchar(100);
    sql_str2 varchar(100);
begin
    sql_str1 := 'select c_name from cur_test_100 where c_id <= 5;';
    sql_str2 := 'select c_city from cur_test_99 where c_num <= 100;';
    open c100 for sql_str;
    close c100;
    open c100 for sql_str;
    close c100;
end;
/

call cursor_ftest_100();
drop table cur_test_100;
drop procedure cursor_ftest_100;

