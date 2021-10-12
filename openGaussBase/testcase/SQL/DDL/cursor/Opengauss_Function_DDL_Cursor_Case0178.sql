--  @testpoint:游标声明在回滚保存点之前，前面打开了的游标在保存点里面，并且游标被一个FETCH命令影响，而这个保存点稍后回滚了，那么这个游标的位置仍然在FETCH让它指向的位置(也就是FETCH不会被回滚)。；

--前置条件
drop table if exists cur_test_178;
create table cur_test_178(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_178 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--定义游标，且在回滚保存点之前,在保存点里打开的游标被fetch影响
start transaction;
cursor cursor178 for select * from cur_test_178 order by 1;
savepoint cursor_savepoint;
fetch 3 from cursor178;
--回滚保存点
rollback to savepoint cursor_savepoint;
--再次提取数据，游标仍在上次fetch指向的位置
fetch from cursor178;
release savepoint cursor_savepoint;
end;


drop table cur_test_178;
