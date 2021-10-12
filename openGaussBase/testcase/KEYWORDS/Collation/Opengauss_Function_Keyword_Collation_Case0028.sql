-- @testpoint: opengauss关键字Collation(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists Collation_test;
create table Collation_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Collation;
create synonym Collation for Collation_test;


--关键字带双引号-成功
drop synonym if exists "Collation";
create synonym "Collation" for Collation_test;
insert into "Collation" values (1,'ada'),(2, 'bob');
update "Collation" set "Collation".name='cici' where "Collation".id=2;
select * from "Collation";

--清理环境
drop synonym "Collation";

--关键字带单引号-合理报错
drop synonym if exists 'Collation';
create synonym 'Collation' for Collation_test;
insert into 'Collation' values (1,'ada'),(2, 'bob');
update 'Collation' set 'Collation'.name='cici' where 'Collation'.id=2;
select * from 'Collation';

--关键字带反引号-合理报错
drop synonym if exists `Collation`;
create synonym `Collation` for Collation_test;
insert into `Collation` values (1,'ada'),(2, 'bob');
update `Collation` set `Collation`.name='cici' where `Collation`.id=2;
select * from `Collation`;
drop table if exists Collation_test;