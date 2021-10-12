--  @testpoint:cursor声明游标，使用select全量查询，指定游标返回的行，返回结果为空，游标提取数据也为空；

--前置条件
drop table if exists cur_test_10;
create table cur_test_10(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));

start transaction;
cursor cursor10 for select * from cur_test_10 order by 1;
fetch from cursor10;
close cursor10;
end;

drop table cur_test_10;

