--  @testpoint:cursor声明游标，游标名为有效参数，符合命名规范；

--前置条件
drop table if exists cur_test_01;
create table cur_test_01(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_01 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--以字母开头
start transaction;
cursor cursor1 for select * from cur_test_01 order by 1;
fetch from cursor1;
close cursor1;
end;

--以下划线开头
start transaction;
cursor _curs1 for select * from cur_test_01 order by 1;
fetch from _curs1;
close _curs1;
end;

--字母数字符号混合
start transaction;
cursor cur#1 for select * from cur_test_01 order by 1;
fetch from cur#1;
close cur#1;
end;

drop table cur_test_01;


