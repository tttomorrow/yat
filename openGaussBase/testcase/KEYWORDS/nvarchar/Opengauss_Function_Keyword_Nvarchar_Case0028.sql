-- @testpoint: opengauss关键字nvarchar(非保留)，作为同义词对象名,部分测试点合理报错

--step1:建表;expect:成功
drop table if exists t_nvarchar_0028;
create table t_nvarchar_0028(id int,name varchar(10));

--step2:关键字不带引号;expect:成功
drop synonym if exists nvarchar;
create synonym nvarchar for t_nvarchar_0028;
insert into nvarchar values (1,'ada'),(2, 'bob');
update nvarchar set nvarchar.name='cici' where nvarchar.id=2;
select * from nvarchar;

--step3:关键字带双引号;expect:成功
drop synonym if exists "nvarchar";
create synonym "nvarchar" for t_nvarchar_0028;

--step4:关键字带单引号;expect:合理报错
drop synonym if exists 'nvarchar';
create synonym 'nvarchar' for t_nvarchar_0028;
insert into 'nvarchar' values (1,'ada'),(2, 'bob');
update 'nvarchar' set 'nvarchar'.name='cici' where 'nvarchar'.id=2;
select * from 'nvarchar';

--step5:关键字带反引号;expect:合理报错
drop synonym if exists `nvarchar`;
create synonym `nvarchar` for t_nvarchar_0028;
insert into `nvarchar` values (1,'ada'),(2, 'bob');
update `nvarchar` set `nvarchar`.name='cici' where `nvarchar`.id=2;
select * from `nvarchar`;

--step6:清理环境;expect:成功
drop synonym if exists "nvarchar";
drop synonym if exists nvarchar;
drop table if exists t_nvarchar_0028;