--  @testpoint:开启事务移动游标位置，初始位置为0，移动游标到前边的一行；

--前置条件
drop table if exists cur_test_173;
create table cur_test_173(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_173 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到前边的一行，提取下一行数据
start transaction;
cursor cursor173 for select * from cur_test_173 order by 1;
move prior from cursor173;
fetch from cursor173;
close cursor173;
end;


drop table cur_test_173;
