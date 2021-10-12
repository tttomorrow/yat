--  @testpoint:开启事务移动游标位置，结果集为空，移动游标到下一行；

--前置条件
drop table if exists cur_test_172;
create table cur_test_172(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));

--结果集为空，移动游标到下一行，可移动，提取数据为空
start transaction;
cursor cursor172 for select * from cur_test_172 order by 1;
move next from cursor172;
fetch from cursor172;
close cursor172;
end;


drop table cur_test_172;
