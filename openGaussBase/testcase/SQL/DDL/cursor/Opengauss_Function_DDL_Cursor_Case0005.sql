-- @testpoint: cursor声明游标，以默认方式（自动判断）检索数据行，参数设为scroll，合理报错；

--前置条件
drop table if exists cur_test_05;
create table cur_test_05(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_05 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

start transaction;
cursor cursor5 scroll for select * from cur_test_05 order by 1;
fetch from cursor5;
close cursor5;
end;

drop table cur_test_05;

