-- @testpoint: cursor声明游标，不以默认方式检索数据行，参数设为no scroll，以倒序方式提取数据，合理报错；

--前置条件
drop table if exists cur_test_07;
create table cur_test_07(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_07 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

start transaction;
cursor cursor7 no scroll for select * from cur_test_07 order by 1;
fetch prior from cursor7;
close cursor7;
end;

drop table cur_test_07;

