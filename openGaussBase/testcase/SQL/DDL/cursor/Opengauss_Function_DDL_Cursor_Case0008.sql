--  @testpoint:cursor声明游标，验证事务结束后游标是否能继续使用，默认参数为without hold，事务结束后游标不可使用(游标自动关闭)，合理报错；

--前置条件
drop table if exists cur_test_08;
create table cur_test_08(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_08 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

start transaction;
cursor cursor8 without hold for select * from cur_test_08 order by 1;
fetch from cursor8;
end;

--继续提取数据，提示cursor不存在
fetch from cursor8;

drop table cur_test_08;

