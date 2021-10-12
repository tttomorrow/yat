--  @testpoint:cursor声明游标，使用select限定条件(group by)查询，指定游标返回的行；

--前置条件
drop table if exists cur_test_14;
create table cur_test_14(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_14 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(21,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAABAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(61,253,'Fendi','Changsha','AAAAABAAAAA');

start transaction;
cursor cursor14 for select count(c_name),c_add from cur_test_14 group by c_add;
fetch from cursor14;
close cursor14;
end;

drop table cur_test_14;


