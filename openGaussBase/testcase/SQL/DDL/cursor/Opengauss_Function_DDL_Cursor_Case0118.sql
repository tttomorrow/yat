--  @testpoint:结合存储过程，显式游标，属性%ISOPEN的使用，游标正常打开；

--前置条件
drop table if exists cur_test_118;
create table cur_test_118(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_118 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标属性%ISOPEN的使用；
drop procedure if exists cursor_ftest_118;
create or replace procedure cursor_ftest_118()
as
declare
    fet_city varchar(10);
    cursor c118 is select c_city from cur_test_118 where c_id <= 5;
begin
    open c118;
    if c118%isopen then
        fetch c118 into fet_city;
        raise info 'fetch results:%',fet_city;
    end if;
    close c118;
end;
/

call cursor_ftest_118();
drop table cur_test_118;
drop procedure cursor_ftest_118;
