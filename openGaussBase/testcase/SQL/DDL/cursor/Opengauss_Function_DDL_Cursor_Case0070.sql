-- @testpoint: declare声明静态游标，指定参数和类型，for指定query；

--前置条件
drop table if exists cur_test_70;
create table cur_test_70(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_70 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');


drop procedure if exists cursor_ftest_70;
create or replace procedure cursor_ftest_70()
as
declare
    cursor c70(c_id int) for select c_name from cur_test_70 where c_id=6;
begin
    open c70(5);
    close c70;
end;
/

drop table cur_test_70;
drop procedure cursor_ftest_70;

