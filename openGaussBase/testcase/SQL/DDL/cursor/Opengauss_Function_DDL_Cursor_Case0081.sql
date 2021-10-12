--  @testpoint:开启事务提取数据，参数为relative count(count>0)，从当前关联位置开始，抓取后面的第count行；

--前置条件
drop table if exists cur_test_81;
create table cur_test_81(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_81 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置
start transaction;
cursor cursor81_1 for select * from cur_test_81 order by 1;
fetch relative 2 from cursor81_1;
close cursor81_1;
end;

--游标move到任意位置，count>0
start transaction;
cursor cursor81_2 for select * from cur_test_81 order by 1;
move forward 3 in cursor81_2;
fetch relative 3 from cursor81_2;
close cursor81_2;
end;


drop table cur_test_81;
