--  @testpoint:关闭所有游标（close all），定义多个游标，查看是否可继续提取数据；

--前置条件
drop table if exists cur_test_177;
create table cur_test_177(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_177 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--定义一个游标，采用close all关闭游标
start transaction;
cursor cursor177_1 for select * from cur_test_177 order by 1;
cursor cursor177_2 for select * from cur_test_177 order by 1;
cursor cursor177_3 for select * from cur_test_177 order by 1;
fetch from cursor177_1;
fetch from cursor177_2;
fetch from cursor177_3;
close all;

--关闭游标后，再次提取数据，合理报错，游标不存在
fetch from cursor177_2;
end;


drop table cur_test_177;
