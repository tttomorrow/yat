--  @testpoint:开启事务提取数据，参数为forward，从当前关联位置开始提取下一行；

--前置条件
drop table if exists cur_test_73;
create table cur_test_73(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_73 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置
start transaction;
cursor cursor73_1 for select * from cur_test_73 order by 1;
fetch forward from cursor73_1;
close cursor73_1;
end;

--移动游标到任意位置
start transaction;
cursor cursor73_2 for select * from cur_test_73 order by 1;
move 3 from cursor73_2;
fetch forward from cursor73_2;
close cursor73_2;
end;

drop table cur_test_73;
