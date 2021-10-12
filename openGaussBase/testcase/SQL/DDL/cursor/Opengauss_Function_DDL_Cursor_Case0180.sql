--  @testpoint:loop循环使用游标,不结合存储过程；

--前置条件
drop table if exists cur_test_180;
create table cur_test_180(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_180 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

begin
    for cursor_180 in (select c_id from cur_test_180 where c_num < 60) loop
        update cur_test_180 set c_name='HAHA';
    end loop;
end;
/

select * from cur_test_180;
drop table cur_test_180;
