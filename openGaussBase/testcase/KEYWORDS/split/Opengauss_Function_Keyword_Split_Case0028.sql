-- @testpoint: opengauss关键字split(保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists split_test;
create table split_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists split;
create synonym split for split_test;
drop synonym if exists split;

--关键字带双引号-成功
drop synonym if exists "split";
create synonym "split" for split_test;
insert into "split" values (1,'ada'),(2, 'bob');
update "split" set "split".name='cici' where "split".id=2;
select * from "split";
drop synonym "split";

--关键字带单引号-合理报错
drop synonym if exists 'split';
create synonym 'split' for split_test;
insert into 'split' values (1,'ada'),(2, 'bob');
update 'split' set 'split'.name='cici' where 'split'.id=2;
select * from 'split';

--关键字带反引号-合理报错
drop synonym if exists `split`;
create synonym `split` for split_test;
insert into `split` values (1,'ada'),(2, 'bob');
update `split` set `split`.name='cici' where `split`.id=2;
select * from `split`;
drop table if exists split_test;