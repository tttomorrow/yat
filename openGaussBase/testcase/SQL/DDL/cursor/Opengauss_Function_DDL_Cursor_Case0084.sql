--  @testpoint:开启事务提取数据，参数为forward count(count<=0)，从当前关联位置开始，抓取前面的abs(count)行；

--前置条件
drop table if exists cur_test_84;
create table cur_test_84(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_84 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置,count<0,抓取前边的abs(count)行
start transaction;
cursor cursor84_1 for select * from cur_test_84 order by 1;
fetch forward -1 from cursor84_1;
fetch forward 0 from cursor84_1;
close cursor84_1;
end;

--游标move到任意位置，count<0,抓取前边的abs(count)行
start transaction;
cursor cursor84_2 for select * from cur_test_84 order by 1;
move forward 3 in cursor84_2;
fetch forward -2 from cursor84_2;
fetch forward 0 from cursor84_2;
close cursor84_2;
end;


drop table cur_test_84;
