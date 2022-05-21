-- @testpoint: 创建枚举类型,标签名测试,部分测试点合理报错

--step1:创建枚举类型,标签名不超过64位   expect:成功
drop type if exists bugstatus;
create type bugstatus as enum ('create', 'modify', 'closed','createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbkhweidhbiwfhbsbcisazd');

--step2:标签名等于64位   expect:失败
drop type if exists bugstatus1 cascade;
create type bugstatus1 as enum ('createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbkhweidhbiwfhbsbcisazdq');

--step3:标签名大于64位   expect:合理报错，报错提示标签名必须在1-63字节
drop type if exists bugstatus1 cascade;
create type bugstatus1 as enum ('createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbkhweidhbiwfhbsbcisazdqf');

--step4:建表，指定其中一列是枚举类型   expect:成功
drop table if exists t_type_0008;
create table t_type_0008(a int, b bugstatus);

--step5.1:插入数据，插入64位的标签   expect:合理报错
insert into t_type_0008 values(1,'createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbkhweidhbiwfhbsbcisazdq');
--step5.2:插入数据，插入63位的标签   expect:成功
insert into t_type_0008 values(1,'createcshksjdbnskjcbnskjcbnsjcbncbsxkcbscbkhweidhbiwfhbsbcisazd');

--step6:查看数据   expect:成功
select * from t_type_0008;

--step7:清理环境   expect:成功
drop table t_type_0008 cascade;
drop type if exists bugstatus cascade;
