--  @testpoint:opengauss关键字inout非保留,存储过程带inout模式

drop table if exists stu_005;
create table stu_005(
id int,
sname varchar2(20),
sage number(2),
ssex varchar2(5)
);

insert into stu_005 values (1,'张三',23,'男');
insert into stu_005 values (2,'李四',23,'男');
insert into stu_005 values (3,'吴鹏',25,'男');
insert into stu_005 values (4,'琴沁',20,'女');
insert into stu_005 values (5,'王丽',20,'女');
insert into stu_005 values (6,'李波',21,'男');
insert into stu_005 values (7,'刘玉',21,'男');
insert into stu_005 values (8,'萧蓉',21,'女');
insert into stu_005 values (9,'陈萧晓',23,'女');
insert into stu_005 values (10,'陈美',22,'女');


DROP PROCEDURE if exists inout_036;

CREATE OR REPLACE PROCEDURE inout_036(P1 in int, num inout int)
IS
begin
select id into num from stu_005 where sage=25;
raise info ':%',num;
EXCEPTION
WHEN NO_DATA_FOUND THEN raise info 'NO_DATA_FOUND';
end;
/
call inout_036(1,1);

drop procedure inout_036;
drop table stu_005;
