--  @testpoint:结合存储过程，定义动态游标，打开动态游标，结合select查询子句命令；

--前置条件
drop table if exists cur_test_102;
create table cur_test_102(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_102 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，定义动态游标，结合select查询子句
drop procedure if exists cursor_ftest_102;
create or replace procedure cursor_ftest_102()
as
declare
    type cursor_type is ref cursor;
    c102 cursor_type;
begin
    open c102 for select c_name from cur_test_102 where c_id <= 5;
    close c102;
end;
/

call cursor_ftest_102();
drop table cur_test_102;
drop procedure cursor_ftest_102;
