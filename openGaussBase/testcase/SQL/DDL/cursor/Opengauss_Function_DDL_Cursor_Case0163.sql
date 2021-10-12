--  @testpoint:开启事务移动游标位置，参数为count，将游标移动到查询中随后的count行；

--前置条件
drop table if exists cur_test_163;
create table cur_test_163(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_163 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询中的count行，count>0，提取下一行数据
start transaction;
cursor cursor163_1 for select * from cur_test_163 order by 1;
move 5 from cursor163_1;
fetch from cursor163_1;
close cursor163_1;
end;

--初始位置，移动游标到查询中的count行，count<0，提取下一行数据
start transaction;
cursor cursor163_2 for select * from cur_test_163 order by 1;
move -3 from cursor163_2;
fetch from cursor163_2;
close cursor163_2;
end;

drop table cur_test_163;
