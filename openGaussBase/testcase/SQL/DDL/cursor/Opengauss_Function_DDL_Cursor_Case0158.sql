--  @testpoint:开启事务移动游标位置，参数为backward，默认从当前关联位置开始，将游标移动到上一行；

--前置条件
drop table if exists cur_test_158;
create table cur_test_158(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_158 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到上一行(移动0行)，提取下一行数据
start transaction;
cursor cursor158_1 for select * from cur_test_158 order by 1;
move backward from cursor158_1;
fetch from cursor158_1;
close cursor158_1;
end;

--移动游标到任意位置，再移动游标到上一行，提取下一行数据
start transaction;
cursor cursor158_2 for select * from cur_test_158 order by 1;
move 3 from cursor158_2;
move backward from cursor158_2;
fetch from cursor158_2;
close cursor158_2;
end;

drop table cur_test_158;
