--  @testpoint:cursor声明游标，同一事务中定义多个不同名游标；


--前置条件
drop table if exists cur_test_31;
create table cur_test_31(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_31 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

start transaction;
cursor cursor31_1 for select * from cur_test_31 order by 1;
cursor cursor31_2 for select * from cur_test_31 order by 1;
cursor cursor31_3 for select * from cur_test_31 order by 1;
fetch from cursor31_1;
fetch from cursor31_2;
fetch from cursor31_3;
close cursor31_1;
close cursor31_2;
close cursor31_3;
end;

drop table cur_test_31;