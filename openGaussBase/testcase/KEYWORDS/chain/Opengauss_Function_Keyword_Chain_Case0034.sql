--  @testpoint:opengauss关键字chain(非保留)，作为游标名
--前置条件
drop table if exists chain_test cascade;
create table chain_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor chain for select * from chain_test order by 1;
close chain;
end;

--关键字带双引号-成功
start transaction;
cursor "chain" for select * from chain_test order by 1;
close "chain";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'chain' for select * from chain_test order by 1;
close 'chain';
end;

--关键字带反引号-合理报错
start transaction;
cursor `chain` for select * from chain_test order by 1;
close `chain`;
end;

--清理环境
drop table chain_test;