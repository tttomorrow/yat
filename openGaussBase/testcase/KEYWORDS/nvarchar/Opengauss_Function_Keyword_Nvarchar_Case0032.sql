-- @testpoint: opengauss关键字nvarchar(非保留);expect:作为用户名 部分测试点合理报错

--step1:关键字explain作为用户名不带引号;expect:创建成功
drop user if exists nvarchar;
create user nvarchar password 'Bigdata@123';
drop user nvarchar;

--step2:关键字explain作为用户名加双引号;expect:创建成功
drop user if exists "nvarchar";
create user "nvarchar" password 'Bigdata@123';
drop user "nvarchar";
 
--step3:关键字explain作为用户名加单引号;expect:合理报错
create user 'nvarchar' password 'Bigdata@123';

--step4:关键字explain作为用户名加反引号;expect:合理报错
create user `nvarchar` password 'Bigdata@123';
