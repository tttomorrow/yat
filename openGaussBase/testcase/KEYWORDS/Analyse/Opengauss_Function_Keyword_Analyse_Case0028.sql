-- @testpoint: opengauss关键字Analyse(保留)，作为同义词对象名,部分测试点合理报错


--前置条件
drop table if exists Analyse_test;
create table Analyse_test(id int,name varchar(10));

--关键字不带引号-失败
drop synonym if exists Analyse;
create synonym Analyse for Analyse_test;


--关键字带双引号-成功
drop synonym if exists "Analyse";
create synonym "Analyse" for Analyse_test;
insert into "Analyse" values (1,'ada'),(2, 'bob');
update "Analyse" set "Analyse".name='cici' where "Analyse".id=2;
select * from "Analyse";

--清理环境
drop synonym "Analyse";

--关键字带单引号-合理报错
drop synonym if exists 'Analyse';
create synonym 'Analyse' for Analyse_test;
insert into 'Analyse' values (1,'ada'),(2, 'bob');
update 'Analyse' set 'Analyse'.name='cici' where 'Analyse'.id=2;
select * from 'Analyse';

--关键字带反引号-合理报错
drop synonym if exists `Analyse`;
create synonym `Analyse` for Analyse_test;
insert into `Analyse` values (1,'ada'),(2, 'bob');
update `Analyse` set `Analyse`.name='cici' where `Analyse`.id=2;
select * from `Analyse`;
drop table if exists Analyse_test;