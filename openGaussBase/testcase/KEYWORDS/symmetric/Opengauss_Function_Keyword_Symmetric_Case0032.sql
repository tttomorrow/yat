--  @testpoint:openGauss保留关键字symmetric作为用户名

--不带引号，合理报错
create user symmetric password 'Bigdata@123';

--openGauss保留关键字symmetric作为 用户名，加双引号，创建成功
drop user if exists "symmetric";
create user "symmetric" password 'Bigdata@123';
drop user "symmetric";

--openGauss保留关键字symmetric作为 用户名，加单引号，合理报错
create user 'symmetric' password 'Bigdata@123';

--openGauss保留关键字symmetric作为 用户名，加反引号，合理报错
create user `symmetric` password 'Bigdata@123';