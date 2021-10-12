--  @testpoint:cursor声明游标，游标名为无效参数，合理报错；

--前置条件
drop table if exists cur_test_02;
create table cur_test_02(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_02 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--以特殊字符开头
start transaction;
cursor #cur for select * from cur_test_01 order by 1;
fetch from #cur;
close #cur;
end;

--以数字开头
start transaction;
cursor 1cur for select * from cur_test_01 order by 1;
fetch from 1cur;
close 1cur;
end;

--字母数字符号混合
start transaction;
cursor $_cur1 for select * from cur_test_01 order by 1;
fetch from $_cur1;
close $_cur1;
end;

drop table cur_test_02;

