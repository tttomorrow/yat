-- @testpoint: 结合游标使用jsonb数据类型

drop table if exists tab130;
create table tab130(c_id int,c_num int,c_name varchar(10),c_add jsonb);
insert into tab130 values
(1,18,'Allen','["Beijing",{"wx":789654123},"AAAAABAAAAA"]'),
(2,368,'Bob','["Shanghai",158,"AAAAACAAAAA"]'),
(3,59,'Cathy','["false","AAAAADAAAAA"]'),
(4,96,'David','["Suzhou","true","AAAAAEAAAAA"]'),
(5,17,'Edrwd','["Fenghuang",null]'),
(6,253,'Fendi','["Changsha",true,"AAAAAGAAAAA"]');

--以字母开头
start transaction;
cursor cursor1 for select * from tab130 order by 4;
fetch from cursor1;
close cursor1;
end;

--以下划线开头
start transaction;
cursor _curs1 for select * from tab130 order by 4;
fetch from _curs1;
close _curs1;
end;

--字母数字符号混合
start transaction;
cursor cur#1 for select * from tab130 order by 4;
fetch from cur#1;
close cur#1;
end;

drop table tab130;