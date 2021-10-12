--  @testpoint:开启事务提取数据，参数为absolute count，游标在任意位置，count小于任意位置，抓取查询中的第count(>0)行，

--前置条件
drop table if exists cur_test_79;
create table cur_test_79(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_79 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--游标move到任意位置，count小于任意位置，count>0
start transaction;
cursor cursor79 for select * from cur_test_79 order by 1;
fetch absolute 1 from cursor79;
move forward 3 from cursor79;
fetch absolute 1 from cursor79;
close cursor79;
end;


drop table cur_test_79;


