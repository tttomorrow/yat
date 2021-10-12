--  @testpoint:开启事务移动游标位置，初始位置为末尾，移动游标到后边的一行；

--前置条件
drop table if exists cur_test_174;
create table cur_test_174(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_174 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--末尾位置，移动游标到后边的一行，提取上一行数据
start transaction;
cursor cursor174 for select * from cur_test_174 order by 1;
move last from cursor174;
move next from cursor174;
fetch prior from cursor174;
close cursor174;
end;


drop table cur_test_174;
