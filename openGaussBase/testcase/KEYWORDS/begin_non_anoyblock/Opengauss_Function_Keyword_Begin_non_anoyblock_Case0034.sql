--  @testpoint:opengauss关键字begin_non_anoyblock(非保留)，作为游标名
--前置条件
drop table if exists begin_non_anoyblock_test cascade;
create table begin_non_anoyblock_test(cid int,fid int);

--关键字不带引号-成功
start transaction;
cursor begin_non_anoyblock for select * from begin_non_anoyblock_test order by 1;
close begin_non_anoyblock;
end;

--关键字带双引号-成功
start transaction;
cursor "begin_non_anoyblock" for select * from begin_non_anoyblock_test order by 1;
close "begin_non_anoyblock";
end;

--关键字带单引号-合理报错
start transaction;
cursor 'begin_non_anoyblock' for select * from begin_non_anoyblock_test order by 1;
close 'begin_non_anoyblock';
end;

--关键字带反引号-合理报错
start transaction;
cursor `begin_non_anoyblock` for select * from begin_non_anoyblock_test order by 1;
close `begin_non_anoyblock`;
end;

--清理环境
drop table begin_non_anoyblock_test;