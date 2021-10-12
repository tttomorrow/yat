--  @testpoint:不开启事务，声明游标,合理报错(游标应该被用在事务块中)；

--前置条件
drop table if exists cur_test_186;
create table cur_test_186(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_186 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--不开启事务，以cursor方式声明游标
cursor cursor_186 for select * from cur_test_186 order by 1;
fetch from cursor_186;
close cursor_186;


drop table cur_test_186;

