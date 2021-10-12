--  @testpoint:cursor声明游标，定义游标类型，类型名为无效值，合理报错(不支持cursor定义类型)；

--前置条件
drop table if exists cur_test_64;
create table cur_test_64(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_64 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--以特殊字符开头
drop function if exists cursor_ftest_64_01;
create or replace function cursor_ftest_64_01()
returns refcursor
as $$
cursor #refcur refcursor;
begin
    open #refcur for select c_name from cur_test_64 where c_id=6;
    return #refcur;
end;
$$ language plpgsql;
/

--以数字开头
drop function if exists cursor_ftest_64_02;
create or replace function cursor_ftest_64_02()
returns refcursor
as $$
cursor 1refcur refcursor;
begin
    open 1refcur for select c_name from cur_test_64 where c_id=6;
    return 1refcur;
end;
$$ language plpgsql;
/


drop table cur_test_64;


