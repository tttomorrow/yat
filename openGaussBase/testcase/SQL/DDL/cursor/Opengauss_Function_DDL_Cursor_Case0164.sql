--  @testpoint:开启事务移动游标位置，参数为relative count，从当前关联位置开始，移动游标到随后或前面的第count行；

--前置条件
drop table if exists cur_test_164;
create table cur_test_164(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_164 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到查询中的第count行，count>0，提取下一行数据
start transaction;
cursor cursor164_1 for select * from cur_test_164 order by 1;
move relative 2 from cursor164_1;
fetch from cursor164_1;
close cursor164_1;
end;

--游标在任意位置，移动游标到查询中的count行，count>0，提取下一行数据
start transaction;
cursor cursor164_2 for select * from cur_test_164 order by 1;
move 2 from cursor164_2;
move relative 1 from cursor164_2;
fetch from cursor164_2;
close cursor164_2;
end;

drop table cur_test_164;
