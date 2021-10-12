--  @testpoint:declare声明动态游标，定义游标类型，类型名为有效值；

--前置条件
drop table if exists cur_test_67;
create table cur_test_67(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_67 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--以字母开头
drop procedure if exists cursor_ftest_67_01;
create or replace procedure cursor_ftest_67_01()
as
declare
    type cursor_type is ref cursor;
    C1 cursor_type;
    sql_str varchar(100);
begin
    sql_str := 'select c_name from cur_test_67 where c_id=6;';
    open C1 for sql_str;
    close C1;
end;
/

--以下划线开头
drop procedure if exists cursor_ftest_67_02;
create or replace procedure cursor_ftest_67_02()
as
declare
    type cursor_type is ref cursor;
    _c1 cursor_type;
    sql_str varchar(100);
begin
    sql_str = 'select c_name from cur_test_67 where c_id=6;';
    open _c1 for sql_str;
end;
/

--字母数字下划线混合
drop procedure if exists cursor_ftest_67_03;
create or replace procedure cursor_ftest_67_03()
as
declare
    type cursor_type is ref cursor;
    c#1 cursor_type;
    sql_str varchar(100);
begin
    sql_str = 'select c_name from cur_test_67 where c_id=6;';
    open c#1 for sql_str;
end;
/

drop table cur_test_67;
drop procedure cursor_ftest_67_01;
drop procedure cursor_ftest_67_02;
drop procedure cursor_ftest_67_03;

