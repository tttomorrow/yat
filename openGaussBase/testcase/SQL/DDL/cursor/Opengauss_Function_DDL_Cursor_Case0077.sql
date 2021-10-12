--  @testpoint:开启事务提取数据，参数为last/absolute -1，抓取查询的最后一行；

--前置条件
drop table if exists cur_test_77;
create table cur_test_77(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_77 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

start transaction;
cursor cursor77_1 for select * from cur_test_77 order by 1;
fetch last from cursor77_1;
close cursor77_1;
end;

start transaction;
cursor cursor77_2 for select * from cur_test_77 order by 1;
fetch absolute -1 from cursor77_2;
close cursor77_2;
end;

drop table cur_test_77;
