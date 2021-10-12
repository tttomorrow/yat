--  @testpoint:opengauss关键字bit(非保留)，作为游标名
--前置条件
drop table if exists bit_test cascade;
create table bit_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor bit for select * from bit_test order by 1;
close bit;
end;

--关键字带双引号-成功
start transaction;
cursor "bit" for select * from bit_test order by 1;
close "bit";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'bit' for select * from bit_test order by 1;
close 'bit';
end;

--关键字带反引号-合理报错
start transaction;
cursor `bit` for select * from bit_test order by 1;
close `bit`;
end;

--清理环境
drop table bit_test;