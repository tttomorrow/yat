-- @testpoint: while loop循环使用游标,结合存储过程,显式游标；
--前置条件
drop table if exists cur_test_184;
create table cur_test_184(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_184 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

drop procedure if exists cursor_ftest_184;
create or replace procedure cursor_ftest_184()
as
declare
    cursor_184 int := 1;
begin
    while cursor_184 < (select c_id from cur_test_184 where c_num = 59) loop
        update cur_test_184 set c_name='HAHA' where c_id = cursor_184;
        cursor_184 := cursor_184+1;
    end loop;
end;
/

call cursor_ftest_184();
select * from cur_test_184;
drop table cur_test_184;
drop procedure if exists cursor_ftest_184;

