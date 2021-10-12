--  @testpoint:游标声明在回滚保存点之后，游标位置不受保存点的影响；

--前置条件
drop table if exists cur_test_179;
create table cur_test_179(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_179 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');


start transaction;
savepoint cursor_savepoint1;
--回滚保存点
rollback to savepoint cursor_savepoint1;
--定义游标，且在回滚保存点之后,游标位置不受之前保存点的影响
cursor cursor179 for select * from cur_test_179 order by 1;
savepoint cursor_savepoint2;
fetch 2 from cursor179;
rollback to cursor_savepoint2;
fetch 1 from cursor179;
release savepoint cursor_savepoint1;
end;


drop table cur_test_179;
