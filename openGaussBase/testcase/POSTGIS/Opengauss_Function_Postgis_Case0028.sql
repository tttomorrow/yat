-- @testpoint: PostGIS功能覆盖,将空间对象输出为Json字符串,ST_AsGeoJson

--step1:创建表   expect:成功
drop table if exists t_postgis_0028;

create table t_postgis_0028 (smgeometry1 geometry(MultiLineString,4490),
                             smgeometry2 geometry(LineString,4490),
                             smgeometry3 geometry(MultiPolygon,4490),
                             smgeometry4 geometry(Polygon,4490),
                             smgeometry5 geometry(MultiPoint,4490),
                             smgeometry6 geometry(Point,4490));

--step2:插入数据   expect:成功
insert into t_postgis_0028 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490),
ST_GeomFromText('LineString(0 0,1 1,1 2)',4490),
ST_GeomFromText('MultiPolygon(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))',4490),
ST_GeomFromText('Polygon((-1 -1, 3 1, 2 3, 0 2,-1 -1))',4490),
ST_GeomFromText('MultiPoint((2 1),(5 3))',4490),
ST_GeomFromText('Point(2 2)',4490));

--step3:结合表查看数据   expect:成功
--将空间对象输出为Json字符串
select ST_AsGeoJson(smgeometry1) from t_postgis_0028;
select ST_AsGeoJson(smgeometry2) from t_postgis_0028;
select ST_AsGeoJson(smgeometry3) from t_postgis_0028;
select ST_AsGeoJson(smgeometry4) from t_postgis_0028;
select ST_AsGeoJson(smgeometry5) from t_postgis_0028;
select ST_AsGeoJson(smgeometry6) from t_postgis_0028;

--step4:清理环境   expect:成功
drop table t_postgis_0028 cascade;
