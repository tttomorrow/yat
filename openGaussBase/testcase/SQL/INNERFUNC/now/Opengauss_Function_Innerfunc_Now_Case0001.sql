-- @testpoint: now()函数用于where条件
select 1 from sys_dummy where now()<>now();
select 1 from sys_dummy where now()!=now();
select 1 from sys_dummy where now()=now();
select 1 from sys_dummy where now() > CURRENT_TIMESTAMP;
select 1 from sys_dummy where now()<CURRENT_TIMESTAMP;
select 1 from sys_dummy where now()<>CURRENT_TIMESTAMP;
select 1 from sys_dummy where now()!=CURRENT_TIMESTAMP;
select 1 from sys_dummy where now()=CURRENT_TIMESTAMP;
select 1 from sys_dummy where now()<=CURRENT_TIMESTAMP;
select 1 from sys_dummy where now()>=CURRENT_TIMESTAMP;
