--  @testpoint:opengauss关键字Authid(保留)，作为同义词对象名


--前置条件
drop table if exists Authid_test;
create table Authid_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Authid;
create synonym Authid for Authid_test;


--关键字带双引号-成功
drop synonym if exists "Authid";
create synonym "Authid" for Authid_test;
insert into "Authid" values (1,'ada'),(2, 'bob');
update "Authid" set "Authid".name='cici' where "Authid".id=2;
select * from "Authid";

--清理环境
drop synonym "Authid";

--关键字带单引号-合理报错
drop synonym if exists 'Authid';
create synonym 'Authid' for Authid_test;
insert into 'Authid' values (1,'ada'),(2, 'bob');
update 'Authid' set 'Authid'.name='cici' where 'Authid'.id=2;
select * from 'Authid';

--关键字带反引号-合理报错
drop synonym if exists `Authid`;
create synonym `Authid` for Authid_test;
insert into `Authid` values (1,'ada'),(2, 'bob');
update `Authid` set `Authid`.name='cici' where `Authid`.id=2;
select * from `Authid`;