--  @testpoint:关闭指定游标名称（close cursor_name），查看是否可继续提取数据；

--前置条件
drop table if exists cur_test_175;
create table cur_test_175(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_175 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--关闭游标，再次提取数据,合理报错，游标不存在
start transaction;
cursor cursor175 for select * from cur_test_175 order by 1;
fetch from cursor175;
close cursor175;
fetch from cursor175;
end;


drop table cur_test_175;
