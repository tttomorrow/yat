-- @testpoint: loop循环使用游标，结合存储过程，隐式游标；
--前置条件
drop table if exists cur_test_182;
create table cur_test_182(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_182 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

drop procedure if exists cursor_ftest_182;
create or replace procedure cursor_ftest_182()
as
declare
    cursor_182 int;
begin
    for cursor_182 in (select c_id from cur_test_182 where c_num < 60) loop
        if sql%found then
            update cur_test_182 set c_name='HAHA' where c_id = cursor_182;
        end if;
    end loop;
end;
/

call cursor_ftest_182();
select * from cur_test_182;
drop table cur_test_182;
drop procedure if exists cursor_ftest_182;
