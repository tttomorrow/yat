--  @testpoint:开启事务移动游标位置，参数为backward count(count<=0)，从当前关联位置开始，移动游标到前边的abs(count)行；

--前置条件
drop table if exists cur_test_169;
create table cur_test_169(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_169 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到后边的第abs(count)行（count<0），提取下一行数据
start transaction;
cursor cursor169_1 for select * from cur_test_169 order by 1;
move backward -2 from cursor169_1;
fetch from cursor169_1;
close cursor169_1;
end;

--游标在任意位置，移动游标到后边的第abs(count)行（count<0），提取下一行数据
start transaction;
cursor cursor169_2 for select * from cur_test_169 order by 1;
move 3 from cursor169_2;
move backward -2 from cursor169_2;
fetch from cursor169_2;
close cursor169_2;
end;

--初始位置，移动游标到后边的第abs(count)行（count=0），提取当前行数据
start transaction;
cursor cursor169_3 for select * from cur_test_169 order by 1;
move backward 0 from cursor169_3;
fetch from cursor169_3;
close cursor169_3;
end;

drop table cur_test_169;
