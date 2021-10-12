-- @testpoint: opengauss关键字chain(非保留)，作为同义词对象名，部分测试点合理报错
--前置条件
drop table if exists chain_test;
create table chain_test(id int,name varchar(10));

--关键字不带引号-成功
drop synonym if exists chain;
create synonym chain for chain_test;
insert into chain values (1,'ada'),(2, 'bob');
update chain set chain.name='cici' where chain.id=2;
select * from chain;

--清理环境
drop synonym if exists chain;

--关键字带双引号-成功
drop synonym if exists "chain";
create synonym "chain" for chain_test;
insert into "chain" values (1,'ada'),(2, 'bob');
update "chain" set "chain".name='cici' where "chain".id=2;
select * from "chain";

--清理环境
drop synonym if exists "chain";

--关键字带单引号-合理报错
drop synonym if exists 'chain';

--关键字带反引号-合理报错
drop synonym if exists `chain`;
drop table if exists chain_test;