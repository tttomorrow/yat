--  @testpoint:开启事务提取数据，参数为backward all ,从当前关联位置开始，抓取所有前面的行；

--前置条件
drop table if exists cur_test_93;
create table cur_test_93(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_93 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--初始位置
start transaction;
cursor cursor93_1 for select * from cur_test_93 order by 1;
fetch backward all from cursor93_1;
close cursor93_1;
end;

--移动游标到任意位置
start transaction;
cursor cursor93_2 for select * from cur_test_93 order by 1;
move 3 from cursor93_2;
fetch backward all in cursor93_2;
close cursor93_2;
end;

drop table cur_test_93;

