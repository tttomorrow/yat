--  @testpoint:开启事务提取数据，初始位置为0，抓取上一行数据，提取为空


--前置条件
drop table if exists cur_test_96;
create table cur_test_96(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_96 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置
start transaction;
cursor cursor96 for select * from cur_test_96;
fetch backward from cursor96;
close cursor96;
end;

drop table cur_test_96;

