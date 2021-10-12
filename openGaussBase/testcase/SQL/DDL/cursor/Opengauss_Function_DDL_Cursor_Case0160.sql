--  @testpoint:开启事务移动游标位置，参数为last，默认从当前关联位置开始，将游标移动到查询的最后一行；

--前置条件
drop table if exists cur_test_160;
create table cur_test_160(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_160 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询的最后一行，提取下一行数据
start transaction;
cursor cursor160_1 for select * from cur_test_160 order by 1;
move last from cursor160_1;
fetch from cursor160_1;
close cursor160_1;
end;

--移动游标到任意位置，再移动游标到查询的最后一行，提取上一行数据
start transaction;
cursor cursor160_2 for select * from cur_test_160 order by 1;
move 3 from cursor160_2;
move last in cursor160_2;
fetch prior from cursor160_2;
close cursor160_2;
end;

drop table cur_test_160;
