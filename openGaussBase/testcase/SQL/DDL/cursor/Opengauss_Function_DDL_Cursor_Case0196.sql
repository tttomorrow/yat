--  @testpoint:创建列存分区表，开启事务声明游标,正向抓取数据，参数为all；

--前置条件
drop table if exists cur_test_196;
create table cur_test_196(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20))
with (orientation=column)
partition by range(c_num)
(partition p1 values less than(50),
partition p2 values less than(100),
partition p3 values less than(150),
partition p4 values less than(maxvalue));

insert into cur_test_196 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--开启事务，声明游标，游标在初始位置，从当前关联位置开始提取所有剩余行的数据
start transaction;
cursor cursor_196_1 for select * from cur_test_196 partition (p2) order by 1;
fetch all from cursor_196_1;
close cursor_196_1;
end;

--开启事务，声明游标，移动游标到任意位置，从当前关联位置开始提取所有剩余行的数据
start transaction;
cursor cursor_196_2 for select * from cur_test_196 partition (p4) order by 1;
move 1 from cursor_196_2;
fetch all from cursor_196_2;
close cursor_196_2;
end;

drop table cur_test_196;
