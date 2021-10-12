--  @testpoint:declare声明游标，定义游标类型，类型名为有效值；

--前置条件
drop table if exists cur_test_65;
create table cur_test_65(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_65 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--以字母开头
drop function if exists cursor_ftest_65_01;
create or replace function cursor_ftest_65_01()
returns refcursor
as $$
declare ref_cursor refcursor;
begin
    open ref_cursor for select c_name from cur_test_65 where c_id=6;
    return ref_cursor;
end;
$$ language plpgsql;
/

--以下划线开头
drop function if exists cursor_ftest_65_02;
create or replace function cursor_ftest_65_02()
returns refcursor
as $$
declare _refcurs refcursor;
begin
    open _refcurs for select c_name from cur_test_65 where c_id=6;
    return _refcurs;
end;
$$ language plpgsql;
/

drop table cur_test_65;
drop function cursor_ftest_65_01;
drop function cursor_ftest_65_02;

