--  @testpoint:开启事务提取数据，游标在末尾位置，抓取下一行数据，提取为空


--前置条件
drop table if exists cur_test_97;
create table cur_test_97(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_97 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--移动游标到结果集末尾位置
start transaction;
cursor cursor97 for select * from cur_test_97;
move last from cursor97;
fetch next from cursor97;
close cursor97;
end;

drop table cur_test_97;

