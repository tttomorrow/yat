-- @testpoint: 时间函数参数数量与指定数量不一致测试, 合理报错
--step1: 测试非法参数数量的时间函数;expect:合理报错
select makedate(1);
select makedate(1, 1, 1);

select maketime(1, 1);
select maketime(1, 1, 1, 1);

select period_add(1);
select period_add(1, 1, 1);

select period_diff(1);
select period_diff(1, 1, 1);

select sec_to_time();
select sec_to_time(1, 1);

select subdate('2022-1-1');
select subdate('2022-1-1', 1, 1);

select subtime('1:1:1');
select subtime('1:1:1', '1:1:1', '1:1:1');

select time();
select time('1:1:1', '1:1:1');

select time_format('1:1:1', '%T', '');
select time_format('1:1:1');

select timediff('1:1:1');
select timediff('1:1:1', '2:2:2', '');

select timestmap();
select timestmap('2000-1-1 1:1:1', '2:2:2', '');

select TIMESTAMPADD(YEAR,1);
select TIMESTAMPADD(YEAR,1,'2022-07-27', '');

select TO_DAYS();
select TO_DAYS('2022-1-1', '');

select TO_SECONDS();
select TO_SECONDS('2022-07-27', '');

select UNIX_TIMESTAMP('2022-07-27', '');

select utc_date(1);
select utc_time(1, 1);
select utc_timestamp(1, 1);