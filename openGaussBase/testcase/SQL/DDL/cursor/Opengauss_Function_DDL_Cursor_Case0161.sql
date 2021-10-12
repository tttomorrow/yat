--  @testpoint:开启事务移动游标位置，参数为absolute count，将游标移动到查询中的count行,count>0；

--前置条件
drop table if exists cur_test_161;
create table cur_test_161(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_161 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询中的count行，提取下一行数据
start transaction;
cursor cursor161_1 for select * from cur_test_161 order by 1;
move absolute 3 from cursor161_1;
fetch from cursor161_1;
close cursor161_1;
end;

--移动游标到任意位置，再移动游标到查询中的count行，提取下一行数据
start transaction;
cursor cursor161_2 for select * from cur_test_161 order by 1;
move 6 from cursor161_2;
move absolute 2 in cursor161_2;
fetch prior from cursor161_2;
close cursor161_2;
end;

drop table cur_test_161;
