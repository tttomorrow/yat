--  @testpoint:开启事务移动游标位置，参数为first，默认从当前关联位置开始，将游标移动到查询的第一行；

--前置条件
drop table if exists cur_test_159;
create table cur_test_159(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_159 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询的第一行，提取下一行数据
start transaction;
cursor cursor159_1 for select * from cur_test_159 order by 1;
move first from cursor159_1;
fetch from cursor159_1;
close cursor159_1;
end;

--移动游标到任意位置，再移动游标到查询的第一行，提取下一行数据
start transaction;
cursor cursor159_2 for select * from cur_test_159 order by 1;
move 3 from cursor159_2;
move first from cursor159_2;
fetch from cursor159_2;
close cursor159_2;
end;

drop table cur_test_159;
