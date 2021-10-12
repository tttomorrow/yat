-- @testpoint: cursor声明游标，使用select限定条件(union)查询，指定游标返回的行；

--前置条件
drop table if exists cur_test_13_01;
drop table if exists cur_test_13_02;
create table cur_test_13_01(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_13_01 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(21,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(61,253,'Fendi','Changsha','AAAAAGAAAAA');

create table cur_test_13_02(c_id int,c_num int,c_name varchar(10),c_city varchar(10));
insert into cur_test_13_02 values(2,22,'Geoge','Hainan'),(32,54,'Hebe','Taiwan'),
                           (12,59,'Ivail','HongKong'),(24,946,'Jack','Shanghai'),
                           (51,117,'Kathy','Qinghai'),(26,253,'Laura','Xian');


start transaction;
cursor cursor13 for
select c_name from cur_test_13_01 where c_id like '%1'
union
select c_name from cur_test_13_02 where c_id like '2%' order by 1;

fetch from cursor13;
close cursor13;
end;

drop table cur_test_13_01;
drop table cur_test_13_02;

