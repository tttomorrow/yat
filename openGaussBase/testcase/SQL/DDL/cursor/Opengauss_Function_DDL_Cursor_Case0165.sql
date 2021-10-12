--  @testpoint:开启事务移动游标位置，参数为relative count，从当前关联位置开始，移动游标到随后或前面的第count行；

--前置条件
drop table if exists cur_test_165;
create table cur_test_165(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_165 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询中的第count行，count<0，提取下一行数据
start transaction;
cursor cursor165_1 for select * from cur_test_165 order by 1;
move relative -2 from cursor165_1;
fetch from cursor165_1;
close cursor165_1;
end;

--游标在任意位置，移动游标到查询中的count行，count<0，提取下一行数据
start transaction;
cursor cursor165_2 for select * from cur_test_165 order by 1;
move 2 from cursor165_2;
move relative -1 from cursor165_2;
fetch from cursor165_2;
close cursor165_2;
end;

--初始位置，移动游标到查询中的第count行，count=0，重复提取当前行数据
start transaction;
cursor cursor165_3 for select * from cur_test_165 order by 1;
move relative 0 from cursor165_3;
fetch from cursor165_3;
close cursor165_3;
end;

drop table cur_test_165;
