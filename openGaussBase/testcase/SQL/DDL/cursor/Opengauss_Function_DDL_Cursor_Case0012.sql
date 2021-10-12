--  @testpoint:cursor声明游标，使用select限定条件(where)查询，指定游标返回的行；

--前置条件
drop table if exists cur_test_12;
create table cur_test_12(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_12 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(21,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(61,253,'Fendi','Changsha','AAAAAGAAAAA');
                           
start transaction;
cursor cursor12 for select * from cur_test_12 where c_id like '%1';
fetch from cursor12;
close cursor12;
end;

drop table cur_test_12;

