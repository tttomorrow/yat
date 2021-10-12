--  @testpoint:开启事务移动游标位置，参数为forward all，从当前关联位置开始，移动游标到最后的行；

--前置条件
drop table if exists cur_test_167;
create table cur_test_167(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_167 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询中的最后一行，提取上一行数据
start transaction;
cursor cursor167_1 for select * from cur_test_167 order by 1;
move forward all from cursor167_1;
fetch prior from cursor167_1;
close cursor167_1;
end;

--游标在任意位置，移动游标到查询中的最后一行，提取上一行数据
start transaction;
cursor cursor167_2 for select * from cur_test_167 order by 1;
move 2 from cursor167_2;
move forward all from cursor167_2;
fetch prior from cursor167_2;
close cursor167_2;
end;


drop table cur_test_167;
