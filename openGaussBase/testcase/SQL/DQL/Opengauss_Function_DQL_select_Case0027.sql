-- @testpoint: DQL语法，结合desc排序

drop table if exists sc;
create table sc(sno varchar2(10),cno varchar2(10),score number(4,2),constraint pk_sc primary key (sno,cno));

insert into sc values ('s001','c001',78.9);
insert into sc values ('s002','c001',80.9);
insert into sc values ('s003','c001',81.9);
insert into sc values ('s004','c001',60.9);
insert into sc values ('s001','c002',82.9);
insert into sc values ('s002','c002',72.9);
insert into sc values ('s003','c002',81.9);
insert into sc values ('s001','c003',59);


select sno from sc where score<80 order by score desc;

drop table sc;

