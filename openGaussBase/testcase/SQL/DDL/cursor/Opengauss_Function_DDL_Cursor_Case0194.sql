--  @testpoint:创建列存表，开启事务声明游标,正向抓取数据，参数为next；

--前置条件
drop table if exists cur_test_194;
create table cur_test_194(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20)) with (orientation=column);
insert into cur_test_194 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--开启事务，声明游标，游标在初始位置，从当前关联位置开始提取下一行数据
start transaction;
cursor cursor_194_1 for select * from cur_test_194 order by 1;
fetch next from cursor_194_1;
close cursor_194_1;
end;

--开启事务，声明游标，移动游标到任意位置，从当前关联位置开始提取下一行数据
start transaction;
cursor cursor_194_2 for select * from cur_test_194 order by 1;
move 3 from cursor_194_2;
fetch next from cursor_194_2;
close cursor_194_2;
end;

drop table cur_test_194;
