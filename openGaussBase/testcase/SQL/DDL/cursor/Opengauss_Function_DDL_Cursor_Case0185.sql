-- @testpoint: while loop循环使用游标,结合存储过程,隐式游标；
--前置条件
drop table if exists cur_test_185;
create table cur_test_185(c_id int,c_num int,c_name varchar(10),c_city varchar(10),c_add varchar(20));
insert into cur_test_185 values(1,18,'Allen','Beijing','AAAAABAAAAA'),(2,368,'Bob','Shanghai','AAAAACAAAAA'),
                           (3,59,'Cathy','Shenzhen','AAAAADAAAAA'),(4,96,'David','Suzhou','AAAAAEAAAAA'),
                           (5,17,'Edrwd','Fenghuang','AAAAAFAAAAA'),(6,253,'Fendi','Changsha','AAAAAGAAAAA');

--结合存储过程&隐式游标%notfound属性
drop procedure if exists cursor_ftest_185;
create or replace procedure cursor_ftest_185()
as
declare
    name varchar(20);
    number int;
    sqlstr varchar(1024);
    type ref_cur_type is ref cursor;
    cur_185 ref_cur_type;
begin
    sqlstr := 'select c_name,c_num from cur_test_185 where c_id <= 5;';
    open cur_185 for sqlstr;
    fetch cur_185 into name, number;
    while cur_185%notfound loop
        raise info 'output：%，%',name,number;
    end loop;
    close cur_185;
END;
/

call cursor_ftest_185();
drop table cur_test_185;
drop procedure if exists cursor_ftest_185;
