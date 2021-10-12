--  @testpoint:开启事务提取数据，参数为absolute count，从末尾抓取查询中的第abs(count)(<=0)行;


--前置条件
drop table if exists cur_test_80;
create table cur_test_80(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_80 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--游标在起始位置，count<=0,从末尾抓取第abs(count)行
start transaction;
cursor cursor80 for select * from cur_test_80 order by 1;
fetch absolute -1 from cursor80;
fetch absolute 0 from cursor80;
close cursor80;
end;

drop table cur_test_80;


