--  @testpoint:结合存储过程，显式游标，属性%ISOPEN的使用，游标未正常打开；

--前置条件
drop table if exists cur_test_119;
create table cur_test_119(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_119 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--创建存储过程，显式游标属性%ISOPEN的使用，游标未打开，%isopen判断为false，不会执行数据提取；
drop procedure if exists cursor_ftest_119;
create or replace procedure cursor_ftest_119()
as
declare
    fet_city varchar(10);
    cursor c119 is select c_city from cur_test_119 where c_id <= 5;
begin
    if c119%isopen then
        fetch c119 into fet_city;
        raise info 'fetch results:%',fet_city;
    end if;
end;
/

call cursor_ftest_119();
drop table cur_test_119;
drop procedure cursor_ftest_119;
