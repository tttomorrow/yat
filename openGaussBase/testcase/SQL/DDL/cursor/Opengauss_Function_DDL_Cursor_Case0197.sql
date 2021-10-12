-- @testpoint: 创建列存分区表，开启事务声明游标,不支持反向抓取数据，参数为prior，合理报错

--前置条件
drop table if exists cur_test_197;
create table cur_test_197(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20))
with (orientation=column)
partition by range(c_num)
(partition p1 values less than(50),
partition p2 values less than(100),
partition p3 values less than(150),
partition p4 values less than(maxvalue));

insert into cur_test_197 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--开启事务，声明游标，游标在初始位置，从当前关联位置开始提取上一行数据，合理报错
start transaction;
cursor cursor_197_1 for select * from cur_test_197 partition (p2) order by 1;
fetch prior from cursor_197_1;
close cursor_197_1;
end;

--开启事务，声明游标，移动游标到任意位置，从当前关联位置开始提取上一行数据，合理报错
start transaction;
cursor cursor_197_2 for select * from cur_test_197 partition (p4) order by 1;
move 1 from cursor_197_2;
fetch prior from cursor_197_2;
close cursor_197_2;
end;

drop table cur_test_197;
