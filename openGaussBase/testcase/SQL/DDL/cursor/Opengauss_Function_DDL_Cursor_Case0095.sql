--  @testpoint:开启事务提取数据，结果集为空时，提取下一行数据，提取到空数据；

--前置条件
drop table if exists cur_test_95;
create table cur_test_95(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));

--初始位置
start transaction;
cursor cursor95 for select * from cur_test_95;
fetch next from cursor95;
close cursor95;
end;

drop table cur_test_95;

