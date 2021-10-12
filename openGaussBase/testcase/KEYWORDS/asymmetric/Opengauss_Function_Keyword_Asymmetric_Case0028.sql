-- @testpoint: opengauss关键字Asymmetric(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists Asymmetric_test;
create table Asymmetric_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Asymmetric;
create synonym Asymmetric for Asymmetric_test;


--关键字带双引号-成功
drop synonym if exists "Asymmetric";
create synonym "Asymmetric" for Asymmetric_test;
insert into "Asymmetric" values (1,'ada'),(2, 'bob');
update "Asymmetric" set "Asymmetric".name='cici' where "Asymmetric".id=2;
select * from "Asymmetric";

--清理环境
drop synonym "Asymmetric";

--关键字带单引号-合理报错
drop synonym if exists 'Asymmetric';
create synonym 'Asymmetric' for Asymmetric_test;
insert into 'Asymmetric' values (1,'ada'),(2, 'bob');
update 'Asymmetric' set 'Asymmetric'.name='cici' where 'Asymmetric'.id=2;
select * from 'Asymmetric';

--关键字带反引号-合理报错
drop synonym if exists `Asymmetric`;
create synonym `Asymmetric` for Asymmetric_test;
insert into `Asymmetric` values (1,'ada'),(2, 'bob');
update `Asymmetric` set `Asymmetric`.name='cici' where `Asymmetric`.id=2;
select * from `Asymmetric`;
drop table if exists Asymmetric_test;