-- @testpoint: DQL语法，结合delete...in

drop table if exists stu;
create table stu(sno varchar2(10) primary key,sname varchar2(20),sage number(2),ssex varchar2(5));
drop table if exists teacher;
create table teacher(tno varchar2(10) primary key,tname varchar2(20));
drop table if exists course;
create table course(cno varchar2(10),cname varchar2(20),tno varchar2(20),constraint pk_course primary key (cno,tno));
drop table if exists sc;
create table sc(sno varchar2(10),cno varchar2(10),score number(4,2),constraint pk_sc primary key (sno,cno));

insert into stu values ('s001','张三',23,'男');
insert into stu values ('s002','李四',23,'男');
insert into stu values ('s003','吴鹏',25,'男');
insert into stu values ('s004','琴沁',20,'女');
insert into stu values ('s005','王丽',20,'女');
insert into stu values ('s006','李波',21,'男');
insert into stu values ('s007','刘玉',21,'男');
insert into stu values ('s008','萧蓉',21,'女');
insert into stu values ('s009','陈萧晓',23,'女');
insert into stu values ('s010','陈美',22,'女');

insert into teacher values ('t001', '刘阳');
insert into teacher values ('t002', '谌燕');
insert into teacher values ('t003', '胡明星');

insert into course values ('c001','J2SE','t002');
insert into course values ('c002','Java Web','t002');
insert into course values ('c003','SSH','t001');
insert into course values ('c004','Oracle','t001');
insert into course values ('c005','SQL SERVER 2005','t003');
insert into course values ('c006','C#','t003');
insert into course values ('c007','JavaScript','t002');
insert into course values ('c008','DIV+CSS','t001');
insert into course values ('c009','PHP','t003');
insert into course values ('c010','EJB3.0','t002');

insert into sc values ('s001','c001',78.9);
insert into sc values ('s002','c001',80.9);
insert into sc values ('s003','c001',81.9);
insert into sc values ('s004','c001',60.9);
insert into sc values ('s001','c002',82.9);
insert into sc values ('s002','c002',72.9);
insert into sc values ('s003','c002',81.9);
insert into sc values ('s001','c003',59);

delete from sc where sc.cno in (select cno from teacher te join course co on (te.tno = co.tno) where te.tname = '谌燕');
select * from sc;

drop table stu;
drop table teacher;
drop table course;
drop table sc;