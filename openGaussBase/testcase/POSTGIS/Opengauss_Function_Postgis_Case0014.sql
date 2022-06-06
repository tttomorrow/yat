-- @testpoint: postgis功能覆盖，查询判断geoga与geogb是否相交,st_intersects

--step1:创建表   expect:成功
drop table if exists t_postgis_0013_01;
drop table if exists t_postgis_0013_02;
drop table if exists t_postgis_0013_03;

create table t_postgis_0013_01 (smgeometry geometry(Point,4490));
create table t_postgis_0013_02 (smgeometry geometry(MultiLineString,4490));
create table t_postgis_0013_03 (smgeometry geometry(MultiPolygon,4490));

--step2:插入数据   expect:成功
insert into t_postgis_0013_01 values(ST_GeomFromText('Point(2 1)',4490));
insert into t_postgis_0013_01 values(ST_GeomFromText('Point(5 9)',4490));

insert into t_postgis_0013_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490));
insert into t_postgis_0013_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 1,2 0,3 1))',4490));
insert into t_postgis_0013_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 2,2 1,3 1))',4490));

insert into t_postgis_0013_03 values(ST_GeomFromText('MultiPolygon(((1 0, 0 1, 1 2, 2 1, 1 0), (2 0, 1 1, 2 2, 3 1, 2 0)))',4490));
insert into t_postgis_0013_03 values(ST_GeomFromText('MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))',4490));
insert into t_postgis_0013_03 values(ST_GeomFromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490));

--step3:查看数据   expect:成功
--判断点线/点面是否相交
select st_intersects(t1.smgeometry,t2.smgeometry) from t_postgis_0013_01 t1,t_postgis_0013_02 t2;
select st_intersects(t1.smgeometry,t3.smgeometry) from t_postgis_0013_01 t1,t_postgis_0013_03 t3;

--查询点线/点面相交个数
select count(*) from (select t1.* from t_postgis_0013_01 t1,t_postgis_0013_02 t2 where st_intersects(t1.smgeometry,t2.smgeometry));
select count(*) from (select t1.* from t_postgis_0013_01 t1,t_postgis_0013_03 t3 where st_intersects(t1.smgeometry,t3.smgeometry));

--step4:清理环境   expect:成功
drop table t_postgis_0013_01 cascade;
drop table t_postgis_0013_02 cascade;
drop table t_postgis_0013_03 cascade;

