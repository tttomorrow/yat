-- @testpoint: loop循环使用游标，结合存储过程，显式游标；

--前置条件
drop table if exists cur_test_181;
create table cur_test_181(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_181 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

drop procedure if exists cursor_ftest_181;
create or replace procedure cursor_ftest_181()
as
declare
    cursor_181 int;
begin
    for cursor_181 in (select c_id from cur_test_181 where c_num < 60) loop
        update cur_test_181 set c_name='HAHA' where c_id = cursor_181;
    end loop;
end;
/

call cursor_ftest_181();
select * from cur_test_181;
drop table cur_test_181;
drop procedure if exists cursor_ftest_181;