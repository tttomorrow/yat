-- @testpoint: opengauss关键字ref(非保留)，作为同义词对象名，部分测试点合理报错


--前置条件
drop table if exists ref_test;
create table ref_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists ref;
create synonym ref for ref_test;
insert into ref values (1,'ada'),(2, 'bob');
update ref set ref.name='cici' where ref.id=2;
select * from ref;
drop synonym if exists ref;

--关键字带双引号-成功
drop synonym if exists "ref";
create synonym "ref" for ref_test;
insert into "ref" values (1,'ada'),(2, 'bob');
update "ref" set "ref".name='cici' where "ref".id=2;
select * from "ref";
drop synonym if exists "ref";

--关键字带单引号-合理报错
drop synonym if exists 'ref';

--关键字带反引号-合理报错
drop synonym if exists `ref`;
drop table if exists ref_test;