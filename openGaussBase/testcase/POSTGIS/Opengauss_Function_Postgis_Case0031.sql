-- @testpoint: PostGIS功能覆盖,将线段上给定位置的点替换为设置的点,部分测试点合理报错
-- @description: ST_SetPoint(geom1,int,geom2),geom1子类型必须为linestring,geom2子类型必须为point

--step1:创建表   expect:成功
drop table if exists t_postgis_0031;

create table t_postgis_0031 (smgeometry1 geometry(MultiLineString,4490),
                             smgeometry2 geometry(LineString,4490),
                             smgeometry3 geometry(Point,4490),
                             smgeometry4 geometry(MultiPoint,4490));

--step2:插入数据   expect:成功
insert into t_postgis_0031 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490),
ST_GeomFromText('LineString(0 0,1 1,1 2)',4490),
ST_GeomFromText('Point(2 2)',4490),
ST_GeomFromText('MultiPoint((1 1),(2 2))',4490));

--step3:结合表查看数据   expect:成功
--将线串中指定位置的点替换为设置的点
select ST_AsEWKT(ST_SetPoint(smgeometry2,0,smgeometry3)) from t_postgis_0031;
select ST_AsEWKT(ST_SetPoint(smgeometry2,1,ST_GeomFromText('Point(-4 -5)',4490))) from t_postgis_0031;

--报错，索引超出范围
select ST_AsEWKT(ST_SetPoint(smgeometry2,3,smgeometry3)) from t_postgis_0031;

--报错，第一个参数必须是linestring
select ST_AsEWKT(ST_SetPoint(smgeometry1,0,smgeometry3)) from t_postgis_0031;
select ST_AsEWKT(ST_SetPoint(smgeometry4,0,smgeometry3)) from t_postgis_0031;

--报错，第二个参数必须是point
select ST_AsEWKT(ST_SetPoint(smgeometry2,0,smgeometry4)) from t_postgis_0031;

--step4:清理环境   expect:成功
drop table t_postgis_0031 cascade;

