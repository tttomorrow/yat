-- @testpoint: 创建行存表以及行存表Gist索引

drop table if exists tablet4;
create table tablet4(c box,d path ,e circle);
insert into tablet4 values('((1,1),(3,3))','((1,1),(1,3),(2,4),(3,3),(4,2),(3,1),(1,1))','((3,3),1)');
DROP INDEX if exists gist_test;
create index gist_test on tablet4 using gist (e);
DROP INDEX if exists gist_test;
drop table if exists tablet4;
