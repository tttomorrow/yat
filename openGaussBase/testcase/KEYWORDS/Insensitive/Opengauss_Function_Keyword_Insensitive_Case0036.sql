-- @testpoint: opengauss关键字Insensitive非保留,创建Insensitive模式游标 合理报错

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


START TRANSACTION;
 CURSOR cursor1 INSENSITIVE FOR SELECT * FROM stu_005 ORDER BY 1;
FETCH FORWARD 3 FROM cursor1;
CLOSE cursor1;
END;
--清理环境
drop table if exists stu_005 cascade;
