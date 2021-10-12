-- @testpoint: 创建列存表，开启事务声明游标,不支持反向抓取数据，参数为为last,合理报错

--前置条件
drop table if exists cur_test_193;
create table cur_test_193(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20)) with (orientation=column);
insert into cur_test_193 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--开启事务，声明游标，游标在初始位置，抓取查询的最后一行数据，合理报错
start transaction;
cursor cursor_193_1 for select * from cur_test_193 order by 1;
fetch last from cursor_193_1;
close cursor_193_1;
end;

--开启事务，声明游标，移动游标到任意位置，抓取查询的最后一行数据，合理报错
start transaction;
cursor cursor_193_2 for select * from cur_test_193 order by 1;
move 3 from cursor_193_2;
fetch last from cursor_193_2;
close cursor_193_2;
end;

drop table cur_test_193;
