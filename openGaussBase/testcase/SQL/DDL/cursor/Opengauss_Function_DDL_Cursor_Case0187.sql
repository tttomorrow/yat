-- @testpoint: 创建列存表，开启事务声明游标,不支持反向抓取数据，参数为backward，合理报错；

--前置条件
drop table if exists cur_test_187;
create table cur_test_187(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20)) with (orientation=column);
insert into cur_test_187 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--开启事务，声明游标，游标在初始位置，backward提取上一行数据，合理报错
start transaction;
cursor cursor_187_1 for select * from cur_test_187 order by 1;
fetch backward from cursor_187_1;
close cursor_187_1;
end;

--开启事务，声明游标，移动游标到任意位置，backward提取上一行数据，合理报错
start transaction;
cursor cursor_187_2 for select * from cur_test_187 order by 1;
move 3 from cursor_187_2;
fetch backward from cursor_187_2;
close cursor_187_2;
end;

drop table cur_test_187;
