--  @testpoint:cursor声明游标，验证事务结束后游标是否能继续使用，参数设为with hold，事务结束后游标仍可使用；

--前置条件
drop table if exists cur_test_09;
create table cur_test_09(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_09 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

start transaction;
cursor cursor9 with hold for select * from cur_test_09 order by 1;
fetch from cursor9;
end;

--继续提取数据，成功
fetch from cursor9;
fetch from cursor9;
close cursor9;

drop table cur_test_09;

