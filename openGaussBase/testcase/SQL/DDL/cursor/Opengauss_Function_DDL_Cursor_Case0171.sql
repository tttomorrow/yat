--  @testpoint:开启事务移动游标位置，结果集为空，移动游标到上一行；

--前置条件
drop table if exists cur_test_171;
create table cur_test_171(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));

--结果集为空，移动游标到上一行，可移动，提取数据为空
start transaction;
cursor cursor171 for select * from cur_test_171 order by 1;
move prior from cursor171;
fetch from cursor171;
close cursor171;
end;


drop table cur_test_171;
