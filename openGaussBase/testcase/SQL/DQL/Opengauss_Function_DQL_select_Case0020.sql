-- @testpoint: DQL语法，结合intersect

drop table if exists stu;
create table stu(sno varchar2(10),sname varchar2(20),sage number(2),ssex varchar2(5));
drop table if exists sc;
create table sc(sno varchar2(10),cno varchar2(10),score number(4,2),constraint pk_sc primary key (sno,cno));

insert into stu values ('s001','张三',23,'男');
insert into stu values ('s002','李四',23,'男');
insert into stu values ('s003','吴鹏',25,'男');
insert into stu values ('s004','琴沁',20,'女');
insert into stu values ('s005','王丽',20,'女');
insert into stu values ('s006','李波',21,'男');
insert into stu values ('s007','刘玉',21,'男');
insert into stu values ('s001','萧蓉',21,'女');
insert into stu values ('s002','陈萧晓',23,'女');
insert into stu values ('s003','陈美',22,'女');

insert into sc values ('s001','c001',78.9);
insert into sc values ('s002','c001',80.9);
insert into sc values ('s003','c001',81.9);
insert into sc values ('s004','c001',60.9);
insert into sc values ('s001','c002',82.9);
insert into sc values ('s002','c002',72.9);
insert into sc values ('s003','c002',81.9);
insert into sc values ('s001','c003',59);


select sno from stu intersect select sno from sc;
select sno from stu intersect all select sno from sc;

drop table stu;
drop table sc;