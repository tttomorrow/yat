--  @testpoint:关闭所有游标（close all），定义一个游标，查看是否可继续提取数据；

--前置条件
drop table if exists cur_test_176;
create table cur_test_176(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_176 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--定义一个游标，采用close all关闭游标，再次提取数据,合理报错，游标不存在
start transaction;
cursor cursor176 for select * from cur_test_176 order by 1;
fetch from cursor176;
close all;
fetch from cursor176;
end;


drop table cur_test_176;
