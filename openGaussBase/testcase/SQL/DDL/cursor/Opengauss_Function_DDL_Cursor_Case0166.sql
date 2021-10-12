--  @testpoint:开启事务移动游标位置，参数为all，从当前关联位置开始，移动游标到最后的行；

--前置条件
drop table if exists cur_test_166;
create table cur_test_166(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_166 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询中的最后一行，提取下一行数据为空
start transaction;
cursor cursor166_1 for select * from cur_test_166 order by 1;
move all from cursor166_1;
fetch from cursor166_1;
close cursor166_1;
end;

--游标在任意位置，移动游标到查询中的最后一行，提取下一行数据为空
start transaction;
cursor cursor166_2 for select * from cur_test_166 order by 1;
move 2 from cursor166_2;
move all from cursor166_2;
fetch from cursor166_2;
close cursor166_2;
end;


drop table cur_test_166;
