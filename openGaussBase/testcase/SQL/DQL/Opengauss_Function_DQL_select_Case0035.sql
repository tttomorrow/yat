-- @testpoint: DQL语法，结合聚集函数和join关联

drop table if exists t_long_or_t12;
drop table if exists t_long_or_t32;
drop table if exists  t_pushdown_t1;
create table t_long_or_t12(F_INT1 int , F_INT2 int);
create table t_long_or_t32(F_INT1 int , F_INT2 int);
create table t_pushdown_t1(F_INT1 INT, F_INT2 INT, F_CHAR CHAR(20), F_INT3 INT, F_INT4 INT, F_INT5 INT, uuid INT NOT NULL);
create index idx_pushdown_id on t_pushdown_t1(uuid);

insert into t_pushdown_t1(uuid, F_INT1, F_INT2, F_CHAR) VALUES(1,1,1,'AAA');
insert into t_long_or_t12(F_INT1, F_INT2) VALUES(1,1);
insert into t_long_or_t12(F_INT1, F_INT2) VALUES(2,1);
insert into t_long_or_t32(F_INT1, F_INT2) VALUES(1,1);
insert into t_long_or_t32(F_INT1, F_INT2) VALUES(2,2);


select linkfiber.fiberUuid as fiberUuid,max(linkfiber.linkName) as linkName,max(route1.F_INT2) as otsUuid from t_long_or_t12 route1 right join (select uuid as fiberUuid, F_CHAR as linkName from t_pushdown_t1 FIBER where FIBER.F_INT1 = 1) linkfiber on route1.F_INT1 = linkfiber .fiberUuid, t_long_or_t32 bidots where route1.F_INT2 = bidots.F_INT2 group by linkfiber.fiberUuid;
 
select linkfiber.fiberUuid as fiberUuid,max(linkfiber.linkName) as linkName,max(route1.F_INT2) as otsUuid from t_long_or_t12 route1 inner join (select uuid as fiberUuid, F_CHAR as linkName from t_pushdown_t1 FIBER where FIBER.F_INT1 = 1) linkfiber on route1.F_INT1 = linkfiber .fiberUuid, t_long_or_t32 bidots where route1.F_INT2 = bidots.F_INT2 group by linkfiber.fiberUuid;

select linkfiber.fiberUuid as fiberUuid,max(linkfiber.linkName) as linkName,max(route1.F_INT2) as otsUuid from t_long_or_t12 route1 full join (select uuid as fiberUuid, F_CHAR as linkName from t_pushdown_t1 FIBER where FIBER.F_INT1 = 1) linkfiber on route1.F_INT1 = linkfiber .fiberUuid, t_long_or_t32 bidots where route1.F_INT2 = bidots.F_INT2 group by linkfiber.fiberUuid;

drop table t_long_or_t12;
drop table t_long_or_t32;
drop table t_pushdown_t1;