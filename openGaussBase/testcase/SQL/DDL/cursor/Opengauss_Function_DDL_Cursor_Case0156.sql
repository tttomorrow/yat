--  @testpoint:开启事务移动游标位置，参数为forward，默认从当前关联位置开始，将游标移动到下一行；

--前置条件
drop table if exists cur_test_156;
create table cur_test_156(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_156 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置，移动游标到下一行，提取下一行数据
start transaction;
cursor cursor156 for select * from cur_test_156 order by 1;
move forward from cursor156;
fetch from cursor156;
close cursor156;
end;

drop table cur_test_156;
